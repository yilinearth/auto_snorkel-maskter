
class Label_Func:
    """A Python class with api functions helping to build label function for the sentiment classification.

    Methods
    ----------
    is_contain_word(data: object, word: str)->bool
        Return true if the word is contained in data.sentence.

    get_word_position(data: object, word: str)->int
        Return the word position in data.sentence.

    is_before_negative_word(data: object, position: int, negative_words: list)->bool:
        Return true if there is negative word appearing before the position in data.sentence.

    """

    def is_contain_word(self, data: object, word: str)->bool:
        """
        :param data: DataFrame
            The input data.
        :param word: str
        :return: bool
            Return true if the word is contained in data.sentence.

        """

    def is_contain_words(self, data: object, word_list: list)->bool:
        """
        :param data: object
            The input data.
        :param word_list: list
            The list of words.
        :return: int
            Return true if there is word in word_list appearing in data.text.

        """

    def get_word_frequency(self, data: object, word: str)->int:
        """
        :param data: object
            The input data.
        :param word: str
        :return: bool
            Return the frequency of the word appearing in the data.text. Notice that all the words is lower-case.
        """

    def get_words_frequency(self, data: object, word_list: list)->int:
        """
        :param data: object
            The input data.
        :param word: str
        :return: bool
            Return the total frequency of all the words in word_list appearing in the data.text. Notice that all the words is lower-case.
        """

    def get_word_position(self, data: object, word: str)->int:
        """
        :param data: DataFrame
            The input data.
        :param word: str
        :return: int
            Return the word position in data.sentence.

        """


