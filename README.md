## Secret Santas

A secret santa web application using Django. This is the final project for CS50's Web Programming with Python and Javascript. 


### Requirements

- Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
- A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.
- A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. Failing that, it should not be submitted; it will be rejected.
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
- Your web application must be mobile-responsive.


### Tools used

- Python Django
- Javascript
- Bootstrap
- Font Awesome (https://fontawesome.com/license)


### Features 

1. Login/Register
    - Only registered users can create groups / join groups
    - Login to create a group
2. Secret Santa Groups
    - Requires at least 3 people - will prompt for addition of more members when there's less than 3 people in the group)
    - View all the groups that the user participates in
    - Become the organiser or a member
    - Set rules such as budget, exchange date and message for the group
    - Editing of group information including addition or removal of members after generating the secret santa list
    - Dynamic reshuffling of secret santas if there's removal/addition of members after drawing of names
3. Browse
    - Choose group wishlist
    - Browse through the different possible gifts of different categories
    - Like a gift to add to wishlist
4. Wishlist
    - Only secret santa of the user can see the user's wishlist
    - Adding of extra note for the user's secret santa
    - Adding / Removal of gifts that can be selected from the Browse page
    

### Distinctiveness and Complexity

This project is distinct and more complicated from all previous projects because:

- Customised notification system for each user (be it for members of  a group or the organiser)
- Smart secret santa algorithm to select the secret santa for each person (dynamically changes the secret santas when there's a change in the listing - reshuffling)
- Nesting of html files (svg animation) inside another html file
- Components (such as editing of pages) shows up only when needed (prevent cluttering of page)
- Appropriate usage of animation when needed, shadows (texture) to achieve a Neumorphic clean user interface 
- More models with complex relation between them
- Creation of HTML elements in javascript and the setting of their attributes 
- Mobile Responsive 



### Files and directories

- `secretsantas` - main application directory
    - `models.py`  - Contains the following models used for the project
        - `User`  - An abstract model with additional attributes `organiser` and `group`
        - `Group` - the user's group/s. Can have multiple groups
        - `Category` - Gift categories
        - `Gift`  - to be added to wishlist
        - `Wishlist` - can be edited by user and can only be viewed by user and user's secret santa
        - `Like` - like/unlike a gift to be added/remove from wishlist
        - `Alert` - Customised notification for user
    - `urls.py` - Contains all url paths 
    - `views.py` - Contains all view functions 
    - `admin.py` - Django admin site (for manipulation of DB)
    - `static/secretsanta` - contains all static content
        - `styles.css` - styling of html files
        - `alert.js` - contain code to mark notification as read (used in `groups.html` and `group.html`)
        - `browse.js` - contain code to load the correct likes, group, addition and removal of gifts from wishlist, liking of gifts, as well as editing of wishlist note
        - `edit.js` - contain code for editing of group information as well as addition and removal of members from group
        - `santas.js` - contain code for adding of input field for user to add more members
        - all files with file extension `.svg` are vector images used for the project
    - `templates/secretsanta` - contains all application templates
        -`browse.html` - page for user to browse the different gifts of different categories and add them to their wishlist
        - `choose.html` - page for user to add members and other information to generate a group
        - `group.html` - individual group information page containing information as budget and exchange date, user can edit the information as well as add/remove members
        - `groups.html` - user's groups which contains information such as whether the group/s have been shuffled and how many members in each group, user can click on the 'more info' button to go into `group.html`
        - `index.html` - landing page which informs users what is the application about and the rules
        - `layout.html` - base template. All other templates extends from it
        - `login.html` - login page
        - `register.html` - registration page
        - following html files are svg animation used for the project
            - `about.html`
            - `box.html`
            - `christmastree.html`
            - `decoration-top.html`
            - `no_wishlist.html`
            - `no_group.html`
            - `rules.html`
            - `stocking.html` 
        
        
### How to run the application 
1. Install Django if it was not installed by running:
    ```pip install -r requirements.txt
2.  ```python3 manage.py makemigrations
3. ```python3 manage.py migrate
4. ```python3 manage.py runserver

#### Adding superuser to have admin access (optional)

1. ```python3 manage.py createsuperuser
2. Add username, email and password


The project's video: https://youtu.be/8Qy0DonNG6I
