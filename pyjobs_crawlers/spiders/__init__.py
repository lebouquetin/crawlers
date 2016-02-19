# -*- coding: utf-8 -*-

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import urlparse
from scrapy.utils.response import get_base_url
from scrapy import Spider, Item, Field, Request
import datetime
from pyjobs_crawlers.items import JobItem


class NotFound(Exception):
    pass


class ParameterNotFound(NotFound):
    pass


class NotCrawlable(Exception):
    pass


class StopCrawlJobList(StopIteration):
    pass


class JobFieldUncomputable(Exception):
    pass


class PublicationDatetimeUncomputable(JobFieldUncomputable):
    @staticmethod
    def fix_job_item(job_item):
        job_item['publication_datetime'] = datetime.datetime.now()
        job_item['publication_datetime_is_fake'] = True


class Tag(object):
    def __init__(self, tag, iteration_nb=1):
        self.tag = tag
        self.weight = iteration_nb


class JobSpider(Spider):
    """Beginning of work"""
    ACTION_START = 'CRAWL_LIST_START'

    """End of work"""
    ACTION_FINISHED = 'CRAWL_LIST_FINISHED'

    """Spider close for other reason of finished"""
    ACTION_UNEXPECTED_END = 'ERROR_UNEXPECTED_END'

    """Crawling job list page"""
    ACTION_CRAWL_LIST = 'CRAWL_LIST'

    """Crawling job page"""
    ACTION_CRAWL_JOB = 'CRAWL_JOB_PAGE'

    """Marker (last crawled point) found: stop crawling"""
    ACTION_MARKER_FOUND = 'CRAWL_LIST_MARKER_FOUND'

    """Something went wrong when crawl"""
    ACTION_CRAWL_ERROR = 'ERROR_CRAWNLING'

    COMMON_TAGS = [
        u'angular',
        u'cdi',
        u'cdd',
        u'django',
        u'flask',
        u'freelance',
        u'hadoop',
        u'javascript'
        u'mysql'
        u'postgresql',
        u'spark',
        u'sql',
        u'stage',
        u'turbogears',
        u'turbo gears',
        u'télétravail',
        u'télé-travail',
        u'web2py',
        u'accessibilité',
        u'ajax',
        u'android',
        u'angular',
        u'angularjs',
        u'angular js',
        u'angular.js',
        u'apache',
        u'backbone.js',
        u'bash',
        u'bootstrap',
        u'cassandra',
        u'centos',
        u'cloud computing',
        u'cms',
        u'couchdb',
        u'crm',
        u'css',
        u'data',
        u'debian',
        u'design pattens',
        u'django',
        u'docker',
        u'drupal',
        u'elasticsearch',
        u'elastic search',
        u'elk',
        u'erp',
        u'ffmpeg',
        u'flume',
        u'git',
        u'gnu',
        u'hadoop',
        u'haproxy',
        u'hbase',
        u'html',
        u'http',
        u'imagemagick',
        u'ios',
        u'j2ee',
        u'java',
        u'javascript',
        u'jenkins',
        u'jira',
        u'jquery',
        u'kafka',
        u'kubernetes',
        u'lamp',
        u'linux',
        u'mapreduce',
        u'mesos',
        u'moa',
        u'mongodb',
        u'mysql',
        u'ness',
        u'node.js',
        u'nosql',
        u'odoo',
        u'openstack',
        u'php',
        u'postgresql',
        u'python',
        u'reactjs',
        u'react.js',
        u'redhat',
        u'responsive-design',
        u'ruby',
        u'ruby on rails',
        u'référencement',
        u'saas',
        u'scala',
        u'seo',
        u'shell',
        u'solr',
        u'spark',
        u'spring',
        u'suse',
        u'swift',
        u'tomcat',
        u'tornado',
        u'ux',
        u'varnish',
        u'versioning',
        u'web',
        u'web services',
        u'websockets',
        u'xhtml',
        u'xml',
        u'zend'
    ]

    CONDITION_TAGS = (
        u'cdd',
        u'cdi',
        u'freelance',
        u'stage',
        u'télétravail',
        u'télé-travail'
    )

    start_urls = []  # To be overwritten
    name = 'no-name'  # To be overwritten
    label = None  # To be overwritten
    url = None  # To be overwritten
    logo_url = None  # To be overwritten
    reformat_url = "{domain}/{found_url}"

    """Job item fields will be filled by overrideable methods"""
    _job_item_fields = [
        'title',
        'publication_datetime',
        'company',
        'company_url',
        'address',
        'description',
        'tags'
    ]

    """Is possible to indicate what a field is collected here (in case of no _crawl_parameters usage)"""
    _forced_collected_field = ()

    """Explicit list of available parameters"""
    _crawl_parameters = {
        'from_page_enabled': True,

        # Xpath version of parameters
        'from_list__jobs_lists__xpath': '//body',
        'from_list__jobs__xpath': None,
        'from_list__url__xpath': None,
        'from_list__next_page__xpath': None,

        'from_list__title__xpath': './h1/text()',
        'from_list__publication_datetime__xpath': None,
        'from_list__company__xpath': None,
        'from_list__company_url__xpath': None,
        'from_list__address__xpath': None,
        'from_list__description__xpath': None,
        'from_list__tags__xpath': None,

        'from_page__container__xpath': '//body',
        'from_page__title__xpath': './h1/text()',
        'from_page__publication_datetime__xpath': None,
        'from_page__company__xpath': None,
        'from_page__company_url__xpath': None,
        'from_page__address__xpath': None,
        'from_page__description__xpath': None,
        'from_page__tags__xpath': None,

        # Css version of parameters
        'from_list__jobs_lists__css': 'body',
        'from_list__jobs__css': None,
        'from_list__url__css': None,
        'from_list__next_page__css': None,

        'from_list__container__css': 'body',
        'from_list__title__css': 'h1',
        'from_list__publication_datetime__css': None,
        'from_list__company__css': None,
        'from_list__company_url__css': None,
        'from_list__address__css': None,
        'from_list__description__css': None,
        'from_list__tags__css': None,

        'from_page__container__css': 'body',
        'from_page__title__css': 'h1',
        'from_page__publication_datetime__css': None,
        'from_page__company__css': None,
        'from_page__company_url__css': None,
        'from_page__address__css': None,
        'from_page__description__css': None,
        'from_page__tags__css': None,
    }

    _requireds = ('title', 'publication_datetime', 'description')

    def __init__(self, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self._connector = None

    @classmethod
    def get_parameter(cls, parameter_name, required=False):
        """

        :param parameter_name: name of parameter
        :param required: if parameter not found or null value will raise ParameterNotFound
        :return: mixed
        """
        if parameter_name not in cls._crawl_parameters:
            if required:
                raise ParameterNotFound("Crawl Parameter \"%s\" is not set")
            return None

        return cls._crawl_parameters[parameter_name]

    @classmethod
    def has_parameter_for_field(cls, field_name):
        if field_name in cls._forced_collected_field:
            return True

        try:
            cls._get_resolved_selector('from_page__' + field_name)
            return True
        except ParameterNotFound:
            pass

        try:
            cls._get_resolved_selector('from_list__' + field_name)
            return True
        except ParameterNotFound:
            pass

        return False

    def _set_crawler(self, crawler):
        super(JobSpider, self)._set_crawler(crawler)
        self._connector = self.settings.get('connector')

    def set_connector(self, connector):
        """

        :param connector: Connecteur
        :return:
        """
        self._connector = connector

    def get_connector(self):
        """

        :return: Connector
        :rtype: pyjobs_crawlers.run.Connector
        """
        if not self._connector:
            raise Exception("_connector attribute is not set")
        return self._connector

    def _build_url(self, response, path):
        base_url = get_base_url(response)
        return urlparse.urljoin(base_url, path)

    def parse(self, response):
        self.get_connector().log(self.name, self.ACTION_START)
        return self.parse_job_list_page(response)

    def parse_job_list_page(self, response):
        """
        Pasring of job list
        """
        self.get_connector().log(self.name, self.ACTION_CRAWL_LIST, response.url)

        try:
            for jobs in self._get_from_list__jobs_lists(response):
                for job in self._get_from_list__jobs(jobs):
                    # first we check url. If the job exists, then skip crawling
                    # (it means that the page has already been crawled
                    try:
                        url = self._get_from_list__url(job)

                    except NotCrawlable:
                        break

                    if self.get_connector().job_exist(url):
                        self.get_connector().log(self.name, self.ACTION_MARKER_FOUND, url)
                        raise StopCrawlJobList()

                    request = Request(url, self.parse_job_page)
                    prefilled_job_item = self._get_prefilled_job_item(job, url)
                    request.meta['item'] = prefilled_job_item

                    if self.is_from_page_enabled():
                        yield request
                    else:
                        yield prefilled_job_item

            next_page_url = self._get_from_list__next_page(response)

            if next_page_url:
                yield Request(url=next_page_url)
        except NotFound, exc:
            self.get_connector().log(self.name, self.ACTION_CRAWL_ERROR, str(exc))
        except StopCrawlJobList:
            pass

    def _get_prefilled_job_item(self, job_node, url):
        """

        :param job_node: html node containg the job
        :return: JobItem filled with founded data
        """
        job_item = JobItem()

        job_item['status'] = JobItem.CrawlStatus.PREFILLED
        job_item['source'] = self.name
        job_item['initial_crawl_datetime'] = datetime.datetime.now()
        job_item['url'] = url

        for job_item_field in self._job_item_fields:
            job_item_method_name = "_get_from_list__%s" % job_item_field
            job_item[job_item_field] = getattr(self, job_item_method_name)(job_node)

        return job_item

    def parse_job_page(self, response):
        """
        Parsing of job page
        """
        self.get_connector().log(self.name, self.ACTION_CRAWL_JOB, response.url)

        job_item = response.meta['item']
        try:
            job_container = self._get_from_page__container(response)
            job_item['url'] = response.url

            for job_item_field in self._job_item_fields:
                if not job_item[job_item_field]:  # Fill field only if not prefilled value
                    job_item_method_name = "_get_from_page__%s" % job_item_field
                    try:
                        job_item[job_item_field] = getattr(self, job_item_method_name)(job_container)
                    except JobFieldUncomputable as exc:
                        exc.fix_job_item(job_item)

        except NotFound, exc:
            # If required extraction fail, we log it
            self.get_connector().log(self.name, self.ACTION_CRAWL_ERROR, str(exc))

        # If some of required job properties are missing, job is INVALID
        if self._item_satisfying(job_item):
            job_item['status'] = JobItem.CrawlStatus.COMPLETED
            # TODO - B.S. - 20160118: Est-ce que l'on yield les INVALID ? Si non ils
            # disparaissent, si oui on les as en bdd mais est-ce pertinent ?
            # Ex. avec lolix ou si on les yield ils polluent la base
            yield job_item
        else:
            job_item['status'] = JobItem.CrawlStatus.INVALID

    #
    # START - Job list page methods
    #

    def _get_from_list__jobs_lists(self, node):
        return self._extract(node, 'from_list__jobs_lists', required=True)

    def _get_from_list__jobs(self, node):
        return self._extract(node, 'from_list__jobs', required=True)

    def _get_from_list__url(self, node):
        extracted_url = self._extract_first(node, 'from_list__url', required=True)
        return self._get_absolute_url(extracted_url)

    def _get_from_list__next_page(self, node):
        return self._extract_first(node, 'from_list__next_page', required=False)

    def _get_from_list__title(self, node):
        return self._extract_first(node, 'from_list__title', required=False)

    def _get_from_list__publication_datetime(self, node):
        if self.is_from_page_enabled():
            return None
        raise PublicationDatetimeUncomputable()

    def _get_from_list__company(self, node):
        return self._extract_first(node, 'from_list__company', required=False)

    def _get_from_list__company_url(self, node):
        return self._extract_first(node, 'from_list__company_url', required=False)

    def _get_from_list__address(self, node):
        return self._extract_first(node, 'from_list__address', required=False)

    def _get_from_list__description(self, node):
        return self._extract_first(node, 'from_list__description', required=False)

    def _get_from_list__tags(self, node):
        tags_html = self._extract_first(node, 'from_list__tags', required=False)
        if tags_html:
            return self.extract_tags(tags_html)
        return []

    #
    # END - Job list page methods
    #

    #
    # START - Job page methods
    #

    def _get_from_page__container(self, node):
        return self._extract(node, 'from_page__container', required=True)

    def _get_from_page__title(self, node):
        return self._extract_first(node, 'from_page__title', required=True)

    def _get_from_page__publication_datetime(self, node):
        raise PublicationDatetimeUncomputable()

    def _get_from_page__company(self, node):
        return self._extract_first(node, 'from_page__company', required=False)

    def _get_from_page__company_url(self, node):
        return self._extract_first(node, 'from_page__company_url', required=False)

    def _get_from_page__address(self, node):
        return self._extract_first(node, 'from_page__address', required=False)

    def _get_from_page__description(self, node):
        return self._extract_first(node, 'from_page__description', required=True)

    def _get_from_page__tags(self, node):
        tags_html = self._extract_first(node, 'from_page__tags', required=False)
        if tags_html:
            return self.extract_tags(tags_html)
        return []

    #
    # END - Job page methods
    #

    def _get_absolute_url(self, url):
        if url.find('http') is 0:
            return url
        parsed_uri = urlparse.urlparse(self.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return self.reformat_url.format(domain=domain, found_url=url)

    def is_from_page_enabled(self):
        from_page_enabled = self.get_parameter('from_page_enabled', required=False)
        return from_page_enabled is None or from_page_enabled

    def _item_satisfying(self, item):
        """
        Return True if required fields are filled, or false if not.
        :param item: JobItem
        :return: bool
        """
        for required_field in self._requireds:
            if not item[required_field]:
                return False
        return True

    def _extract_first(self, container, selector_name, required=True):
        """

        :param container: html node
        :param selector_name: name of selector (without suffix '__xpath' or '__css')
        :param required: if True: if nothing to extracr raise NotFound. Else, return None
        :return: string
        """
        try:
            return ' '.join(self._extract(container, selector_name, required=True).extract_first().split())
        except NotFound:
            if not required:
                return None
            raise

    def _extract_all(self, container, selector_name, required=True):
        """

        :param container: html node
        :param selector_name: name of selector (without suffix '__xpath' or '__css')
        :param required: if True: if nothing to extracr raise NotFound. Else, return None
        :return: list of nodes
        """
        items = []
        try:
            for tag_node in self._extract(container, selector_name, required=True):
                items.append(tag_node.extract().strip())
            return items
        except NotFound:
            if not required:
                return []
            raise

    def _extract(self, container, selector_name, resolve_selector_name=True, selector_type=None, required=True,
                 no_resolve_selector_value=None):
        """

        :param container: html node
        :param selector: xpath or tuple
        :return: Extracted node
        :rtype: scrapy.selector.unified.SelectorList
        """

        if not resolve_selector_name and not selector_type:
            raise Exception('You must set "selector_type" parameter')

        if not resolve_selector_name and not no_resolve_selector_value:
            raise Exception('You must set "no_resolve_selector_value" parameter')

        if resolve_selector_name:
            selector_type, selector = self._get_resolved_selector(selector_name)
        else:
            selector = no_resolve_selector_value

        if isinstance(selector, (list, tuple)):
            for selector_option in selector:
                try:
                    return self._extract(
                            container,
                            selector_name=selector_name,
                            no_resolve_selector_value=selector_option,
                            resolve_selector_name=False,
                            selector_type=selector_type,
                            required=required
                    )
                except NotFound:
                    pass  # We raise after iterate selectors options
            raise NotFound("Can't find list value for %s" % selector_name)

        if selector_type == 'css':
            extract = container.css(selector)
        elif selector_type == 'xpath':
            extract = container.xpath(selector)

        if not extract:
            if required:
                raise NotFound("Can't find value for %s" % selector_name)
            else:
                return None

        # The join of splited text remove \n \t etc ...
        return extract

    @classmethod
    def _get_resolved_selector(cls, selector_name):
        """

        :param selector_name: The name of selector (withour suffix __xpath/__css)
        :return: a tuple containing ('type_of_selector', 'selector_value')
        """
        css_parameter_name = "%s__css" % selector_name
        try:
            return 'css', cls.get_parameter(css_parameter_name, required=True)
        except ParameterNotFound:
            try:
                xpath_parameter_name = "%s__xpath" % selector_name
                return 'xpath', cls.get_parameter(xpath_parameter_name, required=True)
            except ParameterNotFound:
                pass

        raise ParameterNotFound(
                "Crawl Parameter \"%s\" or (\"%s\") is not set" %
                (css_parameter_name, xpath_parameter_name)
        )

    def _extract_common_tags(self, html_content):
        for tag in self.COMMON_TAGS:
            weight = html_content.count(tag)
            if weight:
                yield Tag(tag, weight)

    def extract_specific_tags(self, html_content):
        return []

    def extract_tags(self, html_content):
        html_content = html_content.lower()
        for tag in self._extract_common_tags(html_content):
            yield tag

        for tag in self.extract_specific_tags(html_content):
            yield tag

    def get_crawl_parameters(self):
        return self._crawl_parameters

    @staticmethod
    def _month_french_to_english(datetime_str):
        months = (
            (u'janvier', u'january'),
            (u'février', u'february'),
            (u'mars', u'march'),
            (u'avril', u'april'),
            (u'mai', u'may'),
            (u'juin', u'june'),
            (u'juillet', u'july'),
            (u'août', u'august'),
            (u'septembre', u'september'),
            (u'octobre', u'october'),
            (u'novembre', u'november'),
            (u'décembre', u'december'),

            (u'janv', u'january'),
            (u'févr', u'february'),
            (u'mars', u'march'),
            (u'avril', u'april'),
            (u'avr', u'april'),
            (u'mai', u'may'),
            (u'juin', u'june'),
            (u'juil', u'july'),
            (u'août', u'august'),
            (u'sept', u'september'),
            (u'oct', u'october'),
            (u'nov', u'november'),
            (u'déc', u'december'),
        )

        for key, value in months:
            if key in datetime_str:
                return datetime_str.replace(key, value)
        return datetime_str

    @staticmethod
    def close(spider, reason):
        if reason == 'finished':
            spider.get_connector().log(spider.name, spider.ACTION_FINISHED)
        else:
            spider.get_connector().log(spider.name, spider.ACTION_UNEXPECTED_END, reason)
        return Spider.close(spider, reason)


class JobSource(object):
    def __init__(self, id, label, url, logo_url, spider_class, base_class):
        self.logo_url = logo_url
        self.label = label
        self.id = id
        self.url = url
        self.spider_class = spider_class
        self.base_class = base_class

    @classmethod
    def from_job_spider(cls, job_spider_class, base_class=JobSpider):
        """

        Return a JobSource instance from a pyjobs_crawlers.spiders.JobSpider class

        :param base_class: Class base of spider class
        :param job_spider_class: The JobCrawler class
        :type job_spider_class: pyjobs_crawlers.spiders.JobSpider
        :return: pyjobs_crawlers.JobSource instance
        :rtype: pyjobs_crawlers.spiders.JobSource
        """
        return cls(
                id=job_spider_class.name,
                label=job_spider_class.label,
                url=job_spider_class.url,
                logo_url=job_spider_class.logo_url,
                spider_class=job_spider_class,
                base_class=base_class
        )
