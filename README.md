# SportAttractor - FPL ICT Index public assist

FPL (Fantasy Football(soccer) Premier League) is a game in which users assemble an imaginary team of real life footballers and score points based on those players' actual statistical performance 
or their perceived contribution on the field of play. The [FPL ICT Index](https://www.premierleague.com/news/65567) uses match event data to generate a single view score for each player on three key categories – Influence (player's impact), Creativity (player's producing opportunities) 
and Threat (player's threat on goal). Public users can generate a category card (on either or all of the three key categories) and initiate a discussion. In addition the users insert a Status (Low, Medium, High) to state the degree of importance of that category card.
Current users as well as other users can upvote the categories cards created. Further to a user inserting a Player as a topic in each category card, one can also insert a Feature in each one (ex. dashboard lineups online presence, add feature fouls called on VAR). 

After all, FPL Data Scientists can accumulate all these help data to improve players indices, features stats (goals, assists etc), as well as, platform's features functionalities, appearance and responsiveness. 

## UX

- The strategy plane: 
  - Aim: Achieve a website about Football fans who participate on virtual manager games and Data Scientists to retrieve qualitative weekly sports opinion data specific.
  - Target audience: Football fans in general and Data Scientists interacting with public opinion and accumulate scientific data. 

- The scope plane: 
  - Features
    - Registration and Login section 
    - An initial home page explanation and browse to the three categories
    - Three sections with each categories cards published, create, upvotes and comments
    - A donate section
    - A graphs section demostrating categories numerical stats

- The structure plane: 
  - Info is structured on a standard way and dynamically. One could browse on the categories (buttons) via home page (apart from donate section) or navbar
  - Per category :
    - one could press a button to create a card and through the card, one could post a comment
    - A status [Low, Medium, High] filtering (single, not multiple filtering) and a search text button to find specific cards. 
    - pagination on category cards using linked list concept
  - Donate section implies a credit card form 
  - Graphs section show three charts

- The skeleton plane: 
  - Page info represented from left to right (or top to bottom) concept :
    - Minimal text guidance  
    - Four buttons on home page (three categories and charts)
    - Per category 
      - two buttons (add a card and comment) and pagination (prev and next btns)
      - Three status filtering buttons and a search text input and button submit
      - A back button on view category card to return back to categories cards
    - Button submit donate amount
    - Cross filtered charts

- The surface plane: 
  - Colours : home page showing UK colours and each of the three categories having its distinct colour (blue, white, red)  
  - Semantic : header, nav, section, article, bootswatch (cards, buttons), mark, footer
  - Typography : opens sans google fonts and bootstrap libraries (row, column grid, box model, text centering, flexbox) 
    Iconic and font-awesome icons to assist users to recognize sections 
  - CSS style class helpers, and transitions, animations and opacity for webpage smooth presence and readable text. 

##### User Stories list

- As a developer and user:
  - Show all three categories stats on home page to have a brief overview of their popularity
  - When creating a category card or adding a comment on larger devices, insert a related bg colour thus the input and text area tags are quick easy to target.  

- As a developer :
  - Used UK flag three colours to differentiate the three categories and show game country location (i.e. UK)
  - Used pagination and even numbers per page to not overload the user having many categories per page to scroll
  - As previous and next buttons have been implemented, use page input value to be inserted by the user to achieve flexibility

- As a user : 
  - Category cards posted showing the day that has been created (i.e. Today, 3 days ago etc), to enable me understand the trend and recent topics discussed
    - Above mentioned concept similar concerning each card comments section
  - Number of comments show when viewing a card, thus one can see number of public actions at a glance without scrolling 
  - Use mark tag to highlight the two to three key values on a category card overview

A mockup frame of the website, one could find it at the attached pdf file at the directory mockup_frame. model schema on page 11 inside the pdf file.


## Features


### Existing Features

- Above mentioned on the structure and skeleton plane

---

Additional plans to be implemented in the future would be :

- thread on comments (reply to)
- Database wise, categories classes could all belong in a single model class with an inner column field called category, along with the other current fields  

### Features Left to Implement

- On profile user section, show personal user stats (ex. No of categories, status and comments posted)
- Pagination dropdown form filtering for users to be able to indicate number of category cards displayed per page
- In each category home page, status filter to be multiple, rather than the current single triggered (Lor or Medium or High)
- Datetime on each category footer, showing far from days also the hours ago (specifically if two cards are posted Today).


## Technologies Used

- [Django Python](https://www.djangoproject.com/)
    - The project uses **Django Python and Jinja** for web development.

- Structure WebPage
    - [HTML5]

- Styling WebPage 
    - [CSS3](https://github.com/feddieminas/project_om/blob/master/assets/css/style.css) 
    - [Bootswatch - Bootstrap 4](https://bootswatch.com/flatly/)
    - [Font Awesome 4.7*](https://fontawesome.com/v4.7.0/) and [Open Iconic Bootstrap](https://cdnjs.com/libraries/open-iconic)
 
- [Postgres - SQL](https://www.heroku.com/postgres)
    - The project uses **Postgres - SQL** to be our database resource.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to enable interactivity.

- [D3 JS](https://cdnjs.com/libraries/d3) [DC JS](https://cdnjs.com/libraries/dc)
    - The project uses **D3 - DC JS** for responsive graphs, data type, formats, selecting elements and functions.


## Testing

- Django Py Testcase class to test forms, models and views. The automated Test files could be found inside the apps. 
  - On bash command, one could press ```python3 manage.py test``` for whole test or ```python3 manage.py test <app name>``` per app specific.

- Jasmine Js Testing for the Categories home page pagination and mock ajax page saved last browsed page (page on pagination).

- Having tested it manually, project looks user friendly and works on different browsers and screen sizes. 

----

Encountered issues:

- Cross-browser testing, not all browsers accepted some js selector/style script and switched to jquery selector/style script 

## Deployment

I deployed the project on ....

Worked on Google Chrome and Safari Version.

## Credits


### Content

- The text for readme sales pitch section Fantasy foot explanation were copied from [Fantasy football (association)](https://en.wikipedia.org/wiki/Fantasy_football_(association) and
  from the [FPL ICT Index](https://www.premierleague.com/news/65567).
- Other text content are self-inspired.

### Media

- The categories photos [Influence, Creativity, Threat] were obtained from [influence](https://s.hs-data.com/bilder/teamfotos/640x360/549.jpg), 
  [creativity](https://production-354f.kxcdn.com/wp-content/uploads/sites/10/2018/09/1033628152.jpg), 
  [threat](https://i.guim.co.uk/img/media/f8811e4dfb2c5bcae4730c51f65e96167c541dc1/0_151_2999_1799/master/2999.jpg?width=300&quality=85&auto=format&fit=max&s=45e425c858de26274d39f204f79c37eb).

### Acknowledgements

- I received inspiration for this project from the [Fantasy Premier League](https://fantasy.premierleague.com/). 