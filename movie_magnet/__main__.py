#! /usr/bin/env python3


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from tabulate import tabulate
from termcolor import cprint
from pyfiglet import figlet_format
from random import choice


def get_proxy():
    url = "https://free-proxy-list.net/"
    link = requests.get(url).text
    soup = BeautifulSoup(link, "html.parser")
    table = soup.find("table", id="proxylisttable").find("tbody")
    proxy_list = []
    proxy_https = []
    for row in table.find_all("tr"):
        proxy_data = row.find_all("td")
        proxy_ip = proxy_data[0].text
        proxy_http = "http"
        proxy_list.append(proxy_ip)
        proxy_https.append(proxy_http)

    proxy_list = [{"http": p} for p in proxy_list]
    return proxy_list


def get_magnet(movie_title):
    try:
        proxy = get_proxy()
    except requests.exceptions.ConnectionError:
        print(
            "\n* Connection Error !\nPlease check your internet connection and try again"
        )
        return

    url1 = f"https://thepiratebay10.org/search/{movie_title}/1/99/200"
    size = []
    seeds = []
    seeders = []
    leechers = []
    seeds_error = 0

    for j in range(1, len(proxy) - 1):
        link = requests.get(url1, proxies=proxy[j]).text
        if link != "":
            soup = BeautifulSoup(link, "lxml")
            for tr in soup.find_all("tr"):
                text = tr.find_all("td", {"align": "right", "valign": None})
                seeds.append(text)

            try:
                seeds.pop(0)
                seeds.pop(-1)
            except IndexError:
                print(f"* No movies found with the name {movie_title}!!")
                return

            for i in seeds:
                try:
                    i = str(i)
                    clean_ = re.compile(
                        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"
                    )
                    seeds_ = re.sub(clean_, "", i)
                    seeder_search = re.search(r"\d+", seeds_)
                    leecher_search = re.search(r"\s\d+", seeds_)
                    seeder = seeder_search.group(0)
                    leecher = leecher_search.group(0).strip()
                    seeders.append(int(seeder))
                    leechers.append(int(leecher))

                except:
                    seeds_error += 1

            size_ = soup.find_all("font", class_="detDesc")
            print(f"\nSearching for {movie_title}...")

            results = soup.find_all("div", class_="detName")
            for x in size_:
                size.append(str(x))
            info = []
            for i in size:
                clean = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
                x = re.sub(clean, "", i)
                info.append(x)

            result_video = []
            for i in results:
                result_video.append(i.text)
            date = []
            size1 = []
            date_error = 0
            size_error = 0

            for i in info:
                try:
                    match_date = re.search(r"\d{2}-\d{2}\s\d{4}", i)
                    if match_date:
                        date_ = datetime.datetime.strptime(
                            match_date.group(), "%m-%d %Y"
                        ).date()
                        date.append(date_)
                    else:
                        date.append("")
                except:
                    date_error += 1

                try:
                    match_size = re.search(r"\d+.\d+\s[M|G]+iB", i)
                    if match_size:
                        size1.append(match_size.group(0))
                    else:
                        size1.append("")
                except:
                    size_error += 1

            df = pd.DataFrame()
            ltitle, ldate, lsize, lseeder, lleecher = (
                len(result_video),
                len(date),
                len(size1),
                len(seeders),
                len(leechers),
            )
            max_len = max(ltitle, ldate, lsize, lseeder, lleecher)
            if not max_len == ltitle:
                result_video.extend(["-"] * (max_len - ltitle))
            if not max_len == ldate:
                date.extend(["-"] * (max_len - ldate))
            if not max_len == lsize:
                size1.extend(["-"] * (max_len - lsize))
            if not max_len == lseeder:
                seeders.extend(["-"] * (max_len - lseeder))
            if not max_len == lleecher:
                leechers.extend(["-"] * (max_len - lleecher))
            df["Title"] = result_video
            df["Date"] = date
            df["Size"] = size1
            df["Seeders"] = seeders
            df["Leechers"] = leechers
            df.index = df.index + 1

            print("\nShowing results: \n")

            print(tabulate(df.head(10), headers="keys", tablefmt="fancy_grid"))

            show_more = str(input("Do you want to show more results? (Y/n): "))
            if show_more.lower() in ("yes", "y"):
                print(tabulate(df, headers="keys", tablefmt="psql"))

            print("\nIf you want to download then input the index of the result.")

            while True:
                try:
                    index = int(input("Enter index of the result: "))
                    break
                except ValueError:
                    print("* Only numbers are allowed !!\n")

            name_movie = df["Title"].iloc[index - 1]
            date_movie = df["Date"].iloc[index - 1]
            size_movie = df["Size"].iloc[index - 1]
            seeders_movie = df["Seeders"].iloc[index - 1]
            leechers_movie = df["Leechers"].iloc[index - 1]

            print("\n")
            print(f"Selected Movie:  {name_movie.strip()}")
            print(f"Date:            {date_movie}")
            print(f"Size:            {size_movie}")
            print(f"Seeders:         {seeders_movie}")
            print(f"Leechers:        {leechers_movie}")

            magnet_result = soup.find_all(
                "a", title="Download this torrent using magnet"
            )
            magnet_link = []
            for link in magnet_result:
                magnet_link.append(link["href"])
            download_link = magnet_link[index - 1]

            print(f"\nHere is the magnet link.\n\n{download_link}\n\n")
            input("\nPress Enter key to exit: \n")
            break


if __name__ == "__main__":
    color = choice(
        ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    )

    cprint(
        figlet_format("Movie Magnet", font="standard"), color, attrs=["bold", "dark"]
    )
    cprint("by Fantastic Mouse", color, attrs=["bold", "dark"])

    movie_title = str(input("Please enter what movie you want to search for: "))
    get_magnet(movie_title=movie_title)
