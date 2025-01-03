from dotenv import load_dotenv
load_dotenv()


def get_text_length(str):
    """
    return the length of text
    """
    return len(str)


if __name__ == "__main__":
    print(get_text_length("Hello World"))