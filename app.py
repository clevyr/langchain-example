from dotenv import load_dotenv

# have to load env before importing the app
load_dotenv()

from app import main


if __name__ == '__main__':
    main()
