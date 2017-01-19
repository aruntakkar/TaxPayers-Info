import requests
from bs4 import BeautifulSoup
import datetime
import dropbox


class TransferData:

    def __init__(self, access_token, pins_list):
        self.access_token = access_token
        self.pins_list = pins_list
        self.timestamp = str(datetime.datetime.now()).split('.')[0]


    def get_data_in_file(self):
        """
        	Data Through Web Scrapping is
        	Saved in txt file.
        """

        for pin in self.pins_list:

            url = 'http://www.tinxsys.com/TinxsysInternetWeb/dealerControllerServlet?tinNumber=' + pin + '&searchBy=TIN&backPage=searchByTin_Inter.jsp'

            source = requests.get(url)

            text = source.text

            soup = BeautifulSoup(text, 'html.parser')

            text_from_soup = soup.get_text()

            if "Dealer details by" in text_from_soup:

                header_data = soup.find('td', attrs={'class': "headerBlue"})
                labels_data = soup.findAll('td', attrs={'class': "tdGrey"})
                details_data = soup.findAll('td', attrs={'class': "tdWhite"})

                self.file_name = pin + '-' + self.timestamp + '-' + 'details.txt'

                edited_file = open(self.file_name, 'a')
                edited_file.write(" ".join(header_data.text.split()))

                for label, data in zip(labels_data, details_data):
                    edited_file.write('\n' + " ".join(label.text.split()) + " : " + " ".join(data.text.split()))
                edited_file.close()

            elif "Dealer Not Found" in text_from_soup:
                print("Dealer Not Found for the entered TIN " + pin)


    def uploaded_file(self):
        """
    		Uploading a file to Dropbox
    	"""
        with open(self.file_name, "rb") as File:
            f = File.read()

        dbx = dropbox.Dropbox(self.access_token)

        response = dbx.files_upload(f, '/' + self.timestamp + '/' + self.file_name)

        print('File Uploaded Successfully Response: ', response)


def main():
    """
		Provide your Access Token & Pins List
	"""
    access_token = '' # Put the access token Here

    pins_list = ['07490304055', '07490304053']

    transferData = TransferData(access_token, pins_list)

    transferData.get_data_in_file()

    transferData.uploaded_file()

if __name__ == "__main__":
    main()
