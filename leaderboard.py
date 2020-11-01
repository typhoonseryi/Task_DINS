import click
import requests
import math
import json


def print_some_user(user_id, json_list):
    for user in json_list:
        if user['user_id'] == user_id:
            del user['user_id']
            click.echo(str(user))
            break


def print_country_count(country, json_list):
    country_cnt = 0
    for user in json_list:
        if user['country'] == country:
            country_cnt += 1
    click.echo(str(country_cnt))


def print_all_queryset(json_list, count):
    for user in json_list:
        del user['user_id']
        click.echo(str(user))
    length = len(json_list)
    if count > length:
        click.echo(f'API does not provide as many records ({count}). There are only {length} records.')
    else:
        click.echo(f'There are {length} records.')


def form_json_queryset(mode, count):
    payload = {'mode': mode, 'offset': '0'}
    try:
        data = requests.get('https://www.diabotical.com/api/v0/stats/leaderboard', payload)
    except requests.ConnectionError:
        return 'API is not available'
    try:
        json_page = data.json()['leaderboard']
        len_page = len(json_page)
        if len_page == 0:
            return 'Incorrect game mode'
        if count == -1:
            json_queryset = json_page
        else:
            pages = math.ceil(count / len_page)
            if count <= len_page:
                json_queryset = json_page[:count]
                return json_queryset
            count -= len_page
            page_cnt = 1
            json_pages = json_page
            while page_cnt != pages and len(json_page) != 0:
                offset = page_cnt * len_page
                payload = {'mode': mode, 'offset': offset}
                data = requests.get('https://www.diabotical.com/api/v0/stats/leaderboard', payload)
                json_page = data.json()['leaderboard'][:count]
                count -= len_page
                json_pages.extend(json_page)
                page_cnt += 1
            json_queryset = json_pages
    except (json.decoder.JSONDecodeError, KeyError):
        return 'Something went wrong. Try again'
    return json_queryset


@click.command()
@click.option('--mode', required=True, prompt=True, type=str, help='Type the game mode')
@click.option('--count', default=-1, type=int, help='Type count of users to print')
@click.option('--user_id', type=str, help='Type certain user id')
@click.option('--country', type=str, help='Type country code to count the users')
def main(mode, count, user_id, country):
    json_queryset = form_json_queryset(mode, count)
    if type(json_queryset) == str:
        click.echo(json_queryset)
    elif user_id is None and country is None:
        print_all_queryset(json_queryset, count)
    else:
        if user_id:
            print_some_user(user_id, json_queryset)
        if country:
            print_country_count(country, json_queryset)


if __name__ == "__main__":
    main()