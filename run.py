from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        #bot.change_currency(currency='EUR')
        bot.select_place_to_go(input('Where do you want to go? : '))
        bot.select_date(check_in_date=input('What is the checkin date? (Ex. 29 March 2023) : '),
                        check_out_date=input('What is the checkout date? (Ex. 31 March 2023) : '))
        bot.select_travelers(int(input('How many adults? : ')))
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh()
        bot.report_results()
        input("Bot is finished... Press Enter to quit.")
        bot.close_driver()

except Exception as e:
    if 'in PATH' in str(e):
        print("You are trying to run the bot from command line \n"
              "Please add to PATH your Selenium Drivers \n"
              "Windows: \n"
              "     set PATH=%PATH%;C:path-to-your-folder \n \n"
              "Linux: \n"
              "     set PATH=$PATH:/path/to/your/folder \n \n")
    else:
        raise
