# Word Wise

Word Wise is a web application built with Django that allows users to generate a random word and validate sentences based on the generated word. It utilizes OpenAI's GPT-3.5 language model to provide sentence validation.

## Features

- Generate a random word from the English dictionary
- Submit a sentence and validate it against the generated word using GPT-3.5
- View the result of sentence validation (Valid/Invalid)
- User account creation
- Track user statistics
- Word Wise leaderboard

## Prerequisites

- Python 3.x
- Django
- OpenAI API key

## Installation

1. Clone the repository:
```shell
git clone https://github.com/vtbell21/wordwise.git
```
2. Set up the OpenAI API key:
   * Obtain an API key from OpenAI (https://openai.com).
   * Replace `"YOUR_API_KEY"` with your actual API key in the following files:
       ..* `views.py` - Update the `api_key` variable in the generate_definition function.
3. Set up the database:
   * Run the following commands to create the database tables:
     ```shell
      python manage.py makemigrations
      python manage.py migrate
      ```
## Usage 

1. ```shell
      python manage.py runserver
      ```
2. Access the application in your web browser at 'http://localhost:8000/.'
3. Register a new user account or log in with an existing account.
4. Click the "Generate Random Word" button to generate a random word.
5. Enter a sentence in the provided textarea and click the "Submit" button to validate the sentence.
6. The result of sentence validation (Valid/Invalid) will be displayed.
7. User Statistics:
   * Each user's statistics are recorded and can be viewed on their profile page.
   * Statistics include the total number of attempts and the number of valid and invalid attempts.
8. Word Wise Leaderboard:
   * The Word Wise leaderboard displays the top users with the highest number of valid attempts.
   * Users with the highest number of valid attempts are ranked at the top.
