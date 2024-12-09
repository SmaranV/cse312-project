# Buzzer Beaters 
Link : https://312buzzerbeaters.com/

### Theme Selector
The Theme Selector feature allows users to toggle between Default, Light, and Dark themes. The chosen theme is applied dynamically and saved in the browser, ensuring the user's preference persists across sessions.

#### Testing Procedure
1. Open the app and locate the Theme Selector dropdown.
2. Select "Light" and ensure the background changes to white with black text. The posts' border should be light gray.
3. Select "Dark" and ensure the background changes to dark gray with light text. The posts' border should be darker gray.
4. Select "Default" and ensure the app returns to the original styling (purple background and wheat borders).
5. Refresh the page and confirm the selected theme persists.
6. Clear the browser's `localStorage` and refresh the page. Verify that the Default theme is applied by default.
