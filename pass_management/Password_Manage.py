import random
import string

class PasswordManagement:

    __SpecialCharacters = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '<', '>', '?', '/', '+']

    def __init__(self, special_char=False, pass_length=10, pass_content=None):
        self.__NeedSpecialChar = special_char
        self.__PasswordLength = int(pass_length)
        self.__PasswordContent = pass_content if pass_content else self.__GetContent()
        self.__Password = None

    def __GetContent(self):
        """
        Generate a random string of 5 characters to be used as part of the password content if not provided.
        """
        return ''.join(random.choices(string.ascii_letters, k=5))

    def __GetSpecialPass(self):
        """
        Generate a password with special characters.
        """
        characters = string.ascii_letters + string.digits + ''.join(self.__SpecialCharacters)
        return ''.join(random.choices(characters, k=self.__PasswordLength))

    def __GetPass(self):
        """
        Generate a password without special characters.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=self.__PasswordLength))

    def CreatePassword(self):
        """
        Create a password based on the user's preferences for special characters.
        """
        if self.__NeedSpecialChar:
            password = self.__GetSpecialPass()
        else:
            password = self.__GetPass()

        password_list = list(password) + list(self.__PasswordContent)
        random.shuffle(password_list)
        self.__Password = ''.join(password_list[:self.__PasswordLength])
        return self.__Password
