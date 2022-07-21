# NEW UNTESTED
# From proxy-list.download
# def proxy_list_download_scraper(url, proxy_type, anon):
#     session = requests.session()
#     url = url + "?type=" + proxy_type + "&anon=" + anon
#     html = session.get(url).text
#     if args.verbose:
#         print(url)
#     with open(pathTextFile, "a") as txt_file:
#         for line in html.split("\n"):
#             if len(line) > 0:
#                 txt_file.write(line)