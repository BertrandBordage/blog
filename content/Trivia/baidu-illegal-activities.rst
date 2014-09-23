Baidu illegal activities
========================

:date: 2014-09-23
:tags: security, search engine
:summary: You’re being indhacked.


The facts
---------

What’s Baidu?
~~~~~~~~~~~~~

Baidu is `the most widely <http://chineseseoshifu.com/blog/top-5-chinese-search-engines.html>`_
used search engine in China.
As far as I know, it’s as popular in China as Google is in western countries.
Like any other search engine, Baidu has thousands of bots crawling the web
in order to index everything.

And why do I care about it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my daily job, I read dozens of log entries reporting errors, dead links, and
suspicious operations.  In my case, suspicious operations means attempts of
`IP & referer spoofing <http://en.wikipedia.org/wiki/Spoofing_attack>`_,
`(D)DOS <http://en.wikipedia.org/wiki/Denial-of-service_attack>`_,
and vulnerable software discovery.  The latter means that a bot or someone asks
for pages containing a proof that you use a given version of WordPress, VTiger,
PHPMyAdmin, or any other widely used and quite vulnerable tool.

Most of the time, those reports are triggered by search engine bots like
Google, Bing, Yahoo, or the awful
:abbr:`BnF (Bibliothèque nationale de France)` bot (it fails to rebuild a lot
of URLs from relative links…).

Being indexed by a search engine is generally considered as a good thing:
if your website can’t be found in a simple query on any major search engine,
nobody will reach it.

If your website has an international scope, being indexed by Baidu may be
important, as 500 million people probably use it as their browser homepage.

Baidu crawls… Way too much.
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some nights like tonight, Santa Baidu comes down the chimney and leaves its
marvellous presents in my mailbox.
**Thousands of suspicious operations alerts!**
Cool, it brought me fifty strange requests per minute during all the night!
And even more impressive, each one is different!

It starts with a classical ``/robots.txt``, the best way to find weak points you
shouldn’t look at.

And then it starts spamming stupid PHP/ASP/JSP requests.
I never even used one of these!  Baidu, you offend me.
Here’s a tiny sample of what it asks::

  /do/reg.php
  /wp-content/themes/twentyten/style.css
  /lionsky_client/WebHtmlEditor/1_7_2006_1020/Theme/Office_Tinge/WebHtmlEditor.css
  /ask
  /admin/help/online_help_1.htm
  /Providers/HtmlEditorProviders/Fck/fcklinkgallery.aspx
  /安装说明.txt
  /data/config.js
  /jsp/cis4/js/common/CTRSHTMLElement.js
  /digg.php
  /plugin/backupdb/plugin.xml
  /siteserver/login.aspx
  /a_d/install/data.sql
  /admin/tpls/tpls/main/default/index.tpl
  /ThinkPHP/LICENSE.txt
  /install/data/sql/db_full.sql
  /wcm/app/js/source/wcmlib/WCMConstants.js


An explanation
--------------

Is that so important?
~~~~~~~~~~~~~~~~~~~~~

Yes.

Regular search engine bots don’t do that.  They don’t ask for tens of thousands
of pages in a few hours.  They don’t go to a page that isn’t mentioned
by any other page.

One could argue that it’s not dangerous since these are just regular
HTTP requests: no code injection, no denial of service, no IP spoofing, etc.
That’s right.  And that’s why it’s even more dangerous: Baidu obviously has
a tremendous catalog of software footprints.  Without a single link to those
pages, it knows exactly where to look to know if you’re running PHP, ASP, JSP,
which libraries, and more important, which version of all these.

Of course, these data are totally useless for a search engine; except if it’s
able to tell the user whether a website is technically trustworthy.
But that’s very unlikely.  So why all this?

Baidu doesn’t want to break your website.  It wants to be *able* to do it
at any moment.

A cyberwarfare weapon?
~~~~~~~~~~~~~~~~~~~~~~

Probably…  It could also be a dissuasive weapon, like nuclear missiles.

Do you know `Shodan <http://www.shodanhq.com/>`_?
It’s a very special search engine.
It allows you to find extremely weak servers.
Especially webcam servers without password or with default ones.

That’s truly shocking, but you can spy people you don’t know, learn everything
about their life, and they’re not even aware of being filmed.
If you search and hack enough, I guess you can become the administrator
of a few servers across the globe.

Or you can even control **power plants**, as they’re proud to mention.
That’s obviously not so easy, but it can be done.
It was done in 2010, when `"someone" partially destroyed an Iranian
nuclear plant <http://en.wikipedia.org/wiki/Stuxnet>`_.

As you may know, the US :abbr:`NSA (National Security Agency)` `exploits such
vulnerabilities and even develops hardware
<http://en.wikipedia.org/wiki/NSA_ANT_catalog>`_ to make it easier for them
to infiltrate any online computer.

I honestly don’t have any proof, but I’m sure that China is doing exactly the
same kind of spying & infiltration with tools like Baidu.
I don’t say that Baidu is a covering for illegal government operations.
Maybe all this wasn’t Baidu, but another chinese bot pretending being Baidu.
Or maybe Baidu is simply lead by a bunch of irresponsible hackers.

The solution
------------

Block Baidu, as I did.

In Django, I simply made a middleware.
Add ``'your_project.middleware.ExcludeSuspiciousRequestsMiddleware',`` to your
``MIDDLEWARE_CLASSES`` and put the following in ``your_project/middleware.py``:

.. code-block:: python

    from django.conf import settings
    from django.http import HttpResponse


    BANNED_REFERERS = (
        'http://www.baidu.com',
    )


    class ExcludeSuspiciousRequestsMiddleware(object):
        @staticmethod
        def process_request(request):
            if request.META.get('HTTP_REFERER', None) in BANNED_REFERERS:
                return HttpResponse(
                    'You have been banned from our server. If you think this is a '
                    'miscarriage of justice, ask the admin on '
                    '<a href="mailto:%(@)s">%(@)s</a>.'
                    % {'@': settings.ADMINS[0][1]}, status=403)
