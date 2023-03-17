# Speech-Recognition-Virtual-Assistant-
A virtual assistant for physically handicapped (visually impaired or difficulty with arms to interact with computer)
This code is an implementation of a voice assistant with some functionalities such as opening applications, getting information from Wikipedia, automating a WhatsApp message, and changing the volume/brightness.

The code uses various Python libraries such as pyttsx3 for text to speech conversion, speech_recognition for speech recognition, pywhatkit for WhatsApp automation, pyautogui for GUI automation, and wikipedia for getting information from Wikipedia, and screen_brightness_control for adjusting the system's brightness.

The `speech_to_txt` function uses the `recognize_google` method of the `speech_recognition` library to transcribe the user's speech to text. The recognizeCommand function checks if the transcription was successful and prompts the user to repeat their command if there was an error. The `takeAction` function recognizes the user's command and takes appropriate action.

The program is structured into several functions, including `speech_to_txt` for converting speech input to text, `recognizeCommand` for recognizing the command and taking action, `takeAction` for executing the appropriate function based on the command, and several other functions for opening various apps, searching Wikipedia, and sending WhatsApp messages.

The code uses regular expressions to match patterns in the speech input and determine the appropriate action to take. For example, it matches the pattern "open [a-z]+" to open various apps such as Chrome, Notepad, and Command Prompt, and it matches the pattern "who is [a-z]+" to search for information on a topic on Wikipedia. Various commands are provided along with their uses in the Commands.txt file
