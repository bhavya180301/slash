


<p align="center"><img width="500" src="./assets/slash.png"></p>

[![GitHub license](https://img.shields.io/github/license/Yash-Chandrani/slash)](https://github.com/Yash-Chandrani/slash/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/703241536.svg)](https://zenodo.org/doi/10.5281/zenodo.10023782)
![Github](https://img.shields.io/badge/language-python-red.svg)
[![GitHub issues](https://img.shields.io/github/issues/Yash-Chandrani/slash)](https://github.com/Yash-Chandrani/slash/issues)
[![Github closes issues](https://img.shields.io/github/issues-closed-raw/Yash-Chandrani/slash)](https://github.com/Yash-Chandrani/slash/issues?q=is%3Aissue+is%3Aclosed)
[![Github closed pull requests](https://img.shields.io/github/issues-pr-closed/Yash-Chandrani/slash)](https://github.com/Yash-Chandrani/slash/pulls?q=is%3Apr+is%3Aclosed)
[![codecov](https://codecov.io/gh/Yash-Chandrani/slash/branch/main/graph/badge.svg?token=MGTU44PI4F)](https://codecov.io/gh/Yash-Chandrani/slash)
[![Pylint](https://github.com/Yash-Chandrani/slash/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/Yash-Chandrani/slash/actions/workflows/pylint.yml)
[![Python Style Checker](https://github.com/Yash-Chandrani/slash/actions/workflows/style_checker.yml/badge.svg?branch=main)](https://github.com/Yash-Chandrani/slash/actions/workflows/style_checker.yml)

## Introduction
Meet Slash, not just a tool but a revolution in the world of online shopping. It's designed to transcend the conventional boundaries, promising not only utility but a seamless experience of effortless savings and unparalleled convenience.

## What it Does
Slash redefines how you shop online. No more tedious comparisons across e-commerce platforms—Slash accomplishes it within seconds, giving you back over 50% of your valuable time. Its user-friendly commands make navigating through deals an intuitive and enjoyable process, turning the search for the best deals into a breeze. More than a tool, Slash empowers you with customization, allowing you to tailor your search results instantly. And the excitement doesn't end there—explore our latest releases, the Mini Version and Full Version, ushering in a new era of convenience and efficiency in your online shopping endeavors. Embrace the future of online shopping with Slash, where every click brings you closer to a world of savings and unparalleled satisfaction. Try it now and elevate your online shopping experience!

- 🔄 Easily compare deals across leading e-commerce websites with Slash, streamlining your shopping experience.
- ⏰ Save over 50% of your time by accelerating product search and comparison processes with Slash.
- 🤖 Use simple commands to filter, sort, and search items, ensuring a user-friendly and efficient experience.
- 🎛️ Swiftly modify commands for precise search results, tailoring your shopping experience with ease.
- 🆕 Explore enhanced features and improvements with the latest releases, catering to diverse user preferences.
- ❤️ Easily add desired items to your wishlist for future reference or tracking.
- 💰 Keep track of wishlist items and receive notifications when prices drop, ensuring you never miss a great deal.
- 🌐 Navigate effortlessly from product search to wishlist management, ensuring a smooth shopping journey.
- 🚀 Slash transforms online shopping, making it faster, easier, and more personalized for users with diverse interests.

## Features Added In Phase 5

## Installation Steps 

1. Access the Github repository from your computer. 
 - First, pre-install [git](https://git-scm.com/) on  your machine. 
 - Then, clone the following repo:
 ```
 https://github.com/bhavya180301/slash.git
 ```
 * Finally, ```cd``` into the local repository.
```
cd slash
```
2. Install the ```requirements.txt```. 
- This project uses Python 3, so make sure that [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/stable/installation/) are preinstalled.
- Install the ```requirements.txt``` file using pip.
```
pip3 install -r requirements.txt
```
3. Running the program

- Use the python command to run the ```slash.py``` file.
```
python3 -m src.slash --search socks
```
- To run UI version, execute the following commands
  * cd src/modules
  * python (Inside the python console, implement these commands sequentially)
  * from app  import app,db    
  * app.app_context().push()
  * db.create_all()
  * from app import Users
  * from app import Wishlist
  * db.session.commit()
<p>


## :robot: Increased Code Coverage
We have increased the code coverage from `11%` to `70%`!


## Future Scope
- Can use selenium driver for smoother and faster scraping process.
- Can include an option to check the availability of products in nearby stores.
- Can shift to nosql database.
- Increase the number of filters. Filter by price range and rating range. 


## Use Case
* ***Students***: Students coming to university are generally on a budget and time constraint and generally spend hours wasting time to search for products on Websites. Slash is the perfect tool for these students that slashes all the unnecessary details on a website and helps them get prices for a product across multiple websites.Make the most of this tool in the upcoming Black Friday Sale.
* ***Data Analysts***: Finding data for any project is one of the most tedious job for a data analyst, and the datasets found might not be the most recent one. Using slash, they can create their own dataset in real time and format it as per their needs so that they can focus on what is actually inportant.


## Contribution
Please refer the CONTRIBUTING.md file for instructions on how to contribute to our repository.

## License
This project is licensed under the MIT License.

## Contributors 

<table>
  <tr>
    <td>Group 21</td>
    <td align="center"><a href="https://github.com/bhavya180301/"><img src="https://avatars.githubusercontent.com/u/145395517?v=4" width="80px;" alt=""/><br /><sub><b>Bhavya Harchandani</b></sub></a></td>
    <td align="center"><a href="https://github.com/msethi13/"><img src="https://avatars.githubusercontent.com/u/145397337?v=4" width="80px;" alt=""/><br /><sub><b>Mitali Sethi</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/saxena1701/"><img src="https://avatars.githubusercontent.com/u/143452326?v=4" width="80px;" alt=""/><br /><sub><b>Akshat Saxena</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/sid-ncsu/"><img src="https://avatars.githubusercontent.com/u/142809941?v=4" width="80px;" alt=""/><br /><sub><b>Siddharth Shah</b></sub></a><br /></td>
  </tr>
  </table>

## Funding Information
This project has not yet been funded by any source.

## Support
For any queries and help, please reach out to us at: seproject37@gmail.com

