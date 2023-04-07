# Scrapy settings for job_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'job_scraper'

SPIDER_MODULES = ['job_scraper.spiders']
NEWSPIDER_MODULE = 'job_scraper.spiders'


COOKIES = {
	"__gads": "ID=8ee20878471f2bc2-225eaa6a6fca0047:T=1630562904:S=ALNI_MZ4Zd7YUfH2P_UxQCg0BWrjENZ0nQ",
	"_fbp": "fb.2.1630562903846.713940262",
	"_ga": "GA1.3.747379210.1630562904",
	"_gat_tealium_0": "1",
	"_gcl_au": "1.1.1414545440.1630562901",
	"_gid": "GA1.3.656587558.1631515150",
	"_hjAbsoluteSessionInProgress": "0",
	"_hjDonePolls": "653703",
	"_hjid": "b1dd5dd6-a5a2-47f6-8580-00d2601b543b",
	"_hjIncludedInSessionSample": "0",
	"_legacy_auth0.is.authenticated": "true",
	"_pin_unauth": "dWlkPU1EazROekl5TTJRdE5qSTBZaTAwWldaaUxUZ3paalV0TUdNeU16WmpObU5pTjJNNA",
	"_scid": "c95afa73-e568-4505-a48c-bf131a2fa395",
	"_sctr": "1|1631473200000",
	"adobe_mc": "MCMID=24683204745754252522956201911165223433|MCORGID=199E4673527852240A490D45@AdobeOrg|TS=1631517126",
	"AMCV_199E4673527852240A490D45@AdobeOrg": "-1712354808|MCIDTS|18884|MCMID|24683204745754252522956201911165223433|MCAID|NONE|MCOPTOUT-1631522350s|NONE|MCAAMLH-1632119950|7|MCAAMB-1632119950|j8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI|vVersion|4.3.0|MCSYNCSOP|411-18885",
	"AMCVS_199E4673527852240A490D45@AdobeOrg": "1",
	"amp_7959c4": "V_zM3Wy6etCDEmhB4ZTgCa.NTcyZDgyNzMtOThkNi00OWU5LWFmMWUtZmI2Y2ExYTczZjZh..1fevfh0iv.1fevfh0j1.1.0.1",
	"amp_7959c4_seek.com.au": "V_zM3Wy6etCDEmhB4ZTgCa.NTcyZDgyNzMtOThkNi00OWU5LWFmMWUtZmI2Y2ExYTczZjZh..1fevfh0iv.1fevfh2ks.2.0.2",
	"ASP.NET_SessionId": "fbtzidyvygjrlze1mp25qdkj",
	"auth0.is.authenticated": "true",
	"JobseekerSessionId": "6ee3767178a9dcbcfc98b7eef36ef104",
	"JobseekerVisitorId": "6ee3767178a9dcbcfc98b7eef36ef104",
	"last-known-sol-user-id": "039432ac6cdf2c5b30a90d4bd2bd80ccbc962efda82f59216bf001c6bfd80de768c0ecaee2f51451e79ccd0d8c6b857a72aa5cea72cb72a251cb017bb1dd65efc2ca3fc4a5461c43e80577918813d778c3dc52bb2308bee182fc349db40e8ede192cd396f4aff95c4b8f16d65b8ba39822eb51b99b42299a1e7bf3a6f7420486ac91c69758e8824e594eeae2b8645a6dad2237ba5b602573d273acf4d42089abc4d3d9bed4c5",
	"main": "V|2~P|jobsearch~K|Nurse~WID|3000~W|244~L|3000~OSF|quick&set=1631518539016/V|2~P|jobsearch~WID|3000~L|3000~OSF|quick&set=1630562899708",
	"performed_consent_check": "true",
	"responsive-trial": "firefox:18",
	"s_cc": "true",
	"s_ecid": "MCMID|24683204745754252522956201911165223433",
	"s_ev59": "[['direct','1631518051669']]",
	"s_sq": "[[B]]",
	"searchTerm": "Nurse",
	"skl-lcid": "f3f085a8-8666-4daa-ac3f-b85a582da7d9",
	"sol_id": "63a1f211-cbe2-4bc4-8b32-a49fdbde5d3d",
	"utag_main": "v_id:017ba51f4a950019e97efe8aa8010004c001800900718$_sn:13$_se:16$_ss:0$_st:1631520346354$vapi_domain:seek.com.au$dc_visit:1$ses_id:1631515140194;exp-session$_pn:14;exp-session"
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'job_scraper (+http://www.yourdomain.com)'
# user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'job_scraper.middlewares.JobScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'job_scraper.middlewares.JobScraperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'job_scraper.pipelines.JobScraperPipeline': 300,
	#'job_scraper.pipelines.Firebase': 300
}

DOWNLOADER_MIDDLEWARES = {
    # The priority of 560 is important, because we want this middleware to kick in just before the scrapy built-in `RetryMiddleware`.
    'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
