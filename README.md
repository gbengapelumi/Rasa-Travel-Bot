
# Gdev Travel Assistant Chatbot

This project is a travel assistant chatbot built using Rasa, designed to help users book flights and provide information about their travel plans. The chatbot utilizes intents, entities, and custom actions to facilitate interaction and manage user data effectively.

## Project Structure

The project consists of several key files that define the chatbot's behavior, responses, and rules:

### 1. `domain.yml`

This file defines the **intents**, **entities**, **slots**, and **responses** for the chatbot.

- **Intents**: Represents the purpose of a user's input (e.g., greeting, booking a flight).
- **Entities**: Extracts specific information from user input (e.g., source city, destination city, date).
- **Slots**: Stores values extracted from user input and maintains context throughout the conversation.
- **Responses**: Defines what the chatbot will say in response to various intents.

### 2. `stories.yml`

This file contains predefined conversations (stories) that the chatbot can use to guide interactions with users. Each story outlines a sequence of user intents and corresponding actions taken by the chatbot.

- **Happy Path**: Describes a positive interaction where the user expresses happiness.
- **Sad Paths**: Outline scenarios where the user is unhappy and the chatbot offers support.
- **Booking Ticket**: Guides users through the flight booking process step-by-step.

### 3. `rules.yml`

This file specifies the rules that govern the chatbot's responses to specific intents, ensuring structured interactions.

- **Goodbye Rule**: Defines the action to take when the user says goodbye.
- **Bot Challenge Rule**: Specifies the response when the user questions the chatbot's capabilities.
- **Booking Form Rule**: Manages the flow for submitting the booking form.
- **Activate Booking with Data Rule**: Initiates the booking process based on user input.

### 4. `actions.py`

This file contains custom action classes that implement specific functionality for the chatbot.

- **ActionWeather**: Retrieves and provides weather information based on user location.
- **ActionGreetName**: Greets the user by name if provided.
- **ActionFeedback**: Handles user feedback based on affirmations or denials.
- **ActionGetData**: Fetches flight data based on user-provided details (source, destination, date).

## Dependencies

Ensure you have the following dependencies installed:

- Rasa SDK
- Requests

## Running the Chatbot

To run the chatbot, use the following command:

```bash
rasa run actions
```

In another terminal, start the Rasa server:

```bash
rasa shell
```

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
