Avoid docker-py
===============

:date: 2014-07-27
:tags: python, docker, libraries
:summary: What’s the best way to use Docker with Python?


What’s Docker?
--------------

`Docker <https://www.docker.com/>`_ allows you to easily deploy
a web application anywhere without worrying about which OS or libraries are
installed on the server.  That’s it for the original idea.

But that’s not all.  This simple idea implies a lot of applications.
Personally, I use it for load balancing (using `CoreOS <https://coreos.com/>`_)
and to automatically execute untrusted code in a quite secure environment.
Note that Docker is not perfectly safe for the latter use
(`as stated by the Docker team <https://news.ycombinator.com/item?id=7909622>`_),
but I know the risks…


How to use Docker directly from Python?
---------------------------------------

Docker is normally called using commands like ``docker build -t myimage .``
or ``docker run myimage``.  But if you script your Docker workflow using Python
like I do, you want to find an easy, reliable and robust way to call these
commands inside Python.

You therefore have two solutions:

- `docker-py <https://github.com/docker/docker-py>`_, the official
  Python binding from the Docker team;
- `subprocess.Popen <https://docs.python.org/3/library/subprocess.html#subprocess.Popen>`_,
  the good old way of calling an external program from Python.

That seemed obvious…
~~~~~~~~~~~~~~~~~~~~

At first, docker-py looks very promising.

Not only because it is brought by a team that did a wonderful job on Docker
during the past year, but also because it uses the Docker Remote API.
That means we should be able to easily control Docker through the network
without leaving our comfortable Python.  We can even change the API version
to communicate with an outdated version of Docker!

Another good point: it seems that the syntax is very close to the regular
``docker [command]``.  You just have to initialize a connection with the
Docker daemon, and there you go! ``docker build -t myimage .`` becomes
``c.build('.', 'myimage')``, ``docker commit mycontainer`` becomes
``c.commit('mycontainer')``, etc.

…until you discover the inconsistent, missing, or broken things
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inconsistencies
...............

And it doesn’t take long.  The first thing you realize is that the syntax is
very different from Docker.  You thought ``docker run myimage`` would be
``c.run('myimage')``?  No, that was too easy.
It’s ``ctr = c.create_container`` then ``c.start(ctr)``.

I’m not a docker expert, so I guess there’s a good reason for this choice.
But I don’t think there is a good reason for the following choices.

Second annoyance, half of the commands have different names from their Docker
equivalent.  Some even are split in two.  Nothing terrible here, but still
a bit annoying.

Missing features
................

Now come the real issues.

Some Docker features can’t be used from docker-py.  One has especially driven
me crazy: ``docker run --rm […]``.  With this ``--rm``, Docker will
automatically remove the container when its process has finished, either
normally or after a ``docker kill``.

One would argue: "you just have to kill the container *then* remove it".
Of course, that’s what I did.  But *sometimes*, it doesn’t work perfectly.

Broken things
.............

**And here comes the madness.**

An ``APIError`` is raised by docker-py, stating that the container can’t be removed
because it’s still in use or still moving.  I guess it’s because docker-py
sends a kill request without waiting the end of the real killing,
so sometimes removal happens before the end of kill.  Oddly enough, I noticed
the containers were in fact removed even if an error occurred.  I abhor that,
but I put a ``try\except`` around ``c.remove_container`` to ignore the issue.

But wait!  That’s not all.  ``kill`` only works with running containers,
otherwise it raises an ``APIError`` (and that’s not a bad thing).  Docker has
some tools to inspect a container and therefore know whether it’s running or
not.  I thought I could only kill the container when it’s running.  But no,
according to Docker, the process is always running (in fact, it’s a
`zombie process <http://en.wikipedia.org/wiki/Zombie_process>`_).
And the line after, ``c.kill`` tell us it’s not running… So you have to
add another ``try/except`` around ``c.kill`` to ignore this other exception.
We also need to add a ``c.wait(ctr)`` in order to wait for zombie process to
finish, between ``c.kill`` and ``c.remove_container``.

Instead of this ``try/except``, I decided to add a timeout to decide if a
kill was needed or not.

I wanted to get the output of something like this::

  timeout -s SIGKILL 5 docker run --rm ubuntu:14.04 python3 -c "while True: pass"

And ended up with this:

.. code-block:: python

   from contextlib import contextmanager
   import signal

   import docker
   from docker.errors import APIError

   @contextmanager
   def time_limit(seconds):  # From http://stackoverflow.com/a/601168/1576438
       def signal_handler(signum, frame):
           raise TimeoutException('Timed out!')
       signal.signal(signal.SIGALRM, signal_handler)
       signal.alarm(seconds)
       try:
           yield
       finally:
           signal.alarm(0)

   c = docker.Client()
   ctr = c.create_container('ubuntu:14.04', 'python3 -c "while True: pass"')
   c.start(ctr)

   out = ''
   try:
       with time_limit(5):
           for line in c.logs(ctr, stderr=False, stream=True):
               out += line
   except TimeoutException:
       c.kill(ctr)
   c.wait(ctr)
   try:
       c.remove_container(ctr)
   except APIError:
       pass  # Normally, this should work anyway (and I don’t understand why).


And I had to keep that last ``try/except`` because for an unknown reason,
I still experienced random ``APIErrors``.

At least I had a working version!  Docker was still throwing me some random
warning, but I got what I wanted.

But then something wonderful happened! A docker-py update!  Version 0.3.2,
that should be a few bugfixes.  In my case it wasn’t, I had different bugs.
First, the default API number switched from 1.9 to 1.12.  That’s a major
change, not something you do in a security/bugfix release!  docker-py 0.4.0 was
released one month later, they could have waited…  Basically, updating to 0.3.2
broke everything, especially ``c.logs``.  Changing the API version in
``docker.Client`` to switch back to 1.9 didn’t work either.


Simple solutions are always the best
------------------------------------

After losing 3 full days digging the several issues, I decided to throw
docker-py away in favour of a classical ``subprocess.Popen``.  It took me a few
minutes to get exactly what I wanted.

And it only consists in a few lines:

.. code-block:: python

   from subprocess import Popen, PIPE

   p = Popen(['timeout', '-s', 'SIGKILL', '5', 'docker', 'run', '--rm',
              'ubuntu:14.04', 'python3', '-c', 'while True: pass'],
               stdout=PIPE)
   out = p.stdout.read()
