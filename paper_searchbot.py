# my_author,
# n_of_authors,
# filename,
# title,
# key_word_for_bibliography='REFERENCES'
class PaperSearchBot(object):

    def __init__(self, my_author, n_of_authors, filename, title='', key_word_for_bibliography='REFERENCES'):
        self.my_author = my_author
        self.n_of_authors = n_of_authors
        self.filename = r'C:\Users\Uchek\Desktop\D2 Design\{}'.format(filename)
        self.key_word_for_bibliography = key_word_for_bibliography
        self.content, self.content_list = self.get_content_from_pdf()
        self.titles: 'list[str]' = [
            title] if title != '' else self.get_title_from_content()

    def get_content_from_pdf(self):
        content = str(textract.process(self.filename))
        content = content[content.find(self.key_word_for_bibliography):]
        logger.info(f'''
        ----------------------------------------------------
        {self.key_word_for_bibliography}
        -----------------------------------------------------
        ''')
        content_list = []

        for i in range(len(content) - len(self.my_author)):
            content_list.append(content[i:i + len(self.my_author)])

        return content, content_list

    def get_title_from_content(self):
        content: str = self.content
        content_list: 'list[str]' = self.content_list
        titles: 'list[str]' = []
        references: 'list[str]' = []

        for i in range(content_list.count(self.my_author)):
            instances = content[content.find(
                self.my_author) + len(self.my_author):]
            references.append(content[content.find(
                self.my_author):content.find(self.my_author) + 300])
            content = instances

        for mention in references:
            for _ in range(self.n_of_authors):
                title = mention[mention.find(',') + 1:]
                mention = title
            titles.append(title[:title.find(',')])
        return titles

    def get_paper_of_paper(self):
        self.title = self.titles[0] if type(self.titles[0]) == str else self.titles[int(
            input(f'Is the title one of the following {self.titles}?:'))]

        search_engine = input(
            'which search engine?: 1 -- searchgate, 2 -- sciencedirect, else ---- bing? : ')
        if search_engine == '1':
            self.get_search_gate()
        elif search_engine == '2':
            self.get_science_direct()
        else:
            get_website(f'https://www.bing.com/search?q={self.title}')

    def get_search_gate(self):
        get_website(f'https://www.researchgate.net/search?q={self.title}')
        time.sleep(60*60)

    def get_science_direct(self):
        driver = get_driver('https://www.sciencedirect.com/')
        search_field_button_id_title = 'qs-searchbox-input'
        search_field_button_id_author = 'authors-searchbox-input'
        driver.find_element_by_id(
            search_field_button_id_title).send_keys(self.title)
        driver.find_element_by_id(
            search_field_button_id_author).send_keys(self.my_author)
        driver.find_element_by_css_selector(
            '#aa-srp-search-submit-button > button').click()
        time.sleep(60*60)


def google_scholar_search_paper(title):
    logger.info('''
    if you search for a keyword followed by a wildcard such as flood* it will search for 
    a combination of the letters flood, if you use boolean operators such as keyword1 OR keyword2 it
    expand the search space, if you use AND it will restirct it, use quotation marks
    around the important keywords
    ''')
    url = f'https://scholar.google.co.uk/scholar?hl=en&as_sdt=0%2C5&q={title}'
    get_website(url)
    while True:
        time.sleep(1000)

# ppr = PaperSearchBot(
#     'Klier',
#     8,
#     r'A Steady-State Kinetic Model for Methanol Synthesis and the Water Gas.pdf',
#     'Catalytic synthesis of methanol from COH2'
# )

# ppr.get_paper_of_paper()
