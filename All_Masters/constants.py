# constants.py
COUNTRY_NAMES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Denmark",
    "Djibouti", "Dominica", "Dominican Republic", "East Timor (Timor-Leste)", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
    "Eswatini (fmr. 'Swaziland')", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
    "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Korea (North)", "Korea (South)",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)",
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
    "Oman", "Pakistan", "Palau", "Palestine State", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka",
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
    "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City (Holy See)", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe"
]

UNIT_CODE = ['PCS', 'KGS', 'Box', 'LTR', 'NOS', 'SQFT', 'MTR', 'FOOT', 'SQMTR', 'PAIR', 'BAG', 'PACKET', 'RIM', 'SET', 'MT', 'PER DAY', 'DOZEN', 'JOB', 'SQINCH']



# constants.py
INDIA_STATES_AND_UTS = [
    {"name": "Andhra Pradesh", "code": "28"},
    {"name": "Arunachal Pradesh", "code": "12"},
    {"name": "Assam", "code": "18"},
    {"name": "Bihar", "code": "10"},
    {"name": "Chhattisgarh", "code": "22"},
    {"name": "Goa", "code": "30"},
    {"name": "Gujarat", "code": "24"},
    {"name": "Haryana", "code": "06"},
    {"name": "Himachal Pradesh", "code": "02"},
    {"name": "Jharkhand", "code": "20"},
    {"name": "Karnataka", "code": "29"},
    {"name": "Kerala", "code": "32"},
    {"name": "Madhya Pradesh", "code": "23"},
    {"name": "Maharashtra", "code": "27"},
    {"name": "Manipur", "code": "14"},
    {"name": "Meghalaya", "code": "17"},
    {"name": "Mizoram", "code": "15"},
    {"name": "Nagaland", "code": "13"},
    {"name": "Odisha", "code": "21"},
    {"name": "Punjab", "code": "03"},
    {"name": "Rajasthan", "code": "08"},
    {"name": "Sikkim", "code": "11"},
    {"name": "Tamil Nadu", "code": "33"},
    {"name": "Telangana", "code": "36"},
    {"name": "Tripura", "code": "16"},
    {"name": "Uttar Pradesh", "code": "09"},
    {"name": "Uttarakhand", "code": "05"},
    {"name": "West Bengal", "code": "19"},
    {"name": "Andaman and Nicobar Islands", "code": "92"},
    {"name": "Chandigarh", "code": "94"},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "code": "26"},
    {"name": "Lakshadweep", "code": "31"},
    {"name": "Delhi", "code": "07"},
    {"name": "Puducherry", "code": "34"},
    {"name": "Ladakh", "code": "35"},
    {"name": "Jammu and Kashmir", "code": "01"},
]
############test
CITIES_BY_STATE = {
    1: [
        {"name": "Bhopal"},
        {"name": "Indore"},
        {"name": "Gwalior"},
        # Add more cities
    ],
    2: [
        {"name": "Mumbai"},
        {"name": "Pune"},
        {"name": "Nagpur"},
        # Add more cities
    ],
    # Add more states and their cities
}







CURRENCY_CODES = [
    "AED",  # UAE Dirham
    "AFN",  # Afghan Afghani
    "ALL",  # Albanian Lek
    "AMD",  # Armenian Dram
    "ANG",  # Netherlands Antillean Guilder
    "AOA",  # Angolan Kwanza
    "ARS",  # Argentine Peso
    "AUD",  # Australian Dollar
    "AWG",  # Aruban Florin
    "AZN",  # Azerbaijani Manat
    "BAM",  # Bosnia and Herzegovina Convertible Mark
    "BBD",  # Barbadian Dollar
    "BDT",  # Bangladeshi Taka
    "BGN",  # Bulgarian Lev
    "BHD",  # Bahraini Dinar
    "BIF",  # Burundian Franc
    "BMD",  # Bermudian Dollar
    "BND",  # Brunei Dollar
    "BOB",  # Bolivian Boliviano
    "BRL",  # Brazilian Real
    "BSD",  # Bahamian Dollar
    "BTN",  # Bhutanese Ngultrum
    "BWP",  # Botswanan Pula
    "BYN",  # Belarusian Ruble
    "BZD",  # Belize Dollar
    "CAD",  # Canadian Dollar
    "CDF",  # Congolese Franc
    "CHF",  # Swiss Franc
    "CLP",  # Chilean Peso
    "CNY",  # Chinese Yuan
    "COP",  # Colombian Peso
    "CRC",  # Costa Rican Colón
    "CUC",  # Cuban Convertible Peso
    "CUP",  # Cuban Peso
    "CVE",  # Cape Verdean Escudo
    "CZK",  # Czech Koruna
    "DJF",  # Djiboutian Franc
    "DKK",  # Danish Krone
    "DOP",  # Dominican Peso
    "DZD",  # Algerian Dinar
    "EGP",  # Egyptian Pound
    "ERN",  # Eritrean Nakfa
    "ETB",  # Ethiopian Birr
    "EUR",  # Euro
    "FJD",  # Fijian Dollar
    "FKP",  # Falkland Islands Pound
    "FOK",  # Faroese Króna
    "GBP",  # British Pound Sterling
    "GEL",  # Georgian Lari
    "GHS",  # Ghanaian Cedi
    "GIP",  # Gibraltar Pound
    "GMD",  # Gambian Dalasi
    "GNF",  # Guinean Franc
    "GTQ",  # Guatemalan Quetzal
    "GYD",  # Guyanaese Dollar
    "HKD",  # Hong Kong Dollar
    "HNL",  # Honduran Lempira
    "HRK",  # Croatian Kuna
    "HTG",  # Haitian Gourde
    "HUF",  # Hungarian Forint
    "IDR",  # Indonesian Rupiah
    "ILS",  # Israeli New Shekel
    "INR",  # Indian Rupee
    "IQD",  # Iraqi Dinar
    "IRR",  # Iranian Rial
    "ISK",  # Icelandic Króna
    "JMD",  # Jamaican Dollar
    "JOD",  # Jordanian Dinar
    "JPY",  # Japanese Yen
    "KES",  # Kenyan Shilling
    "KGS",  # Kyrgystani Som
    "KHR",  # Cambodian Riel
    "KID",  # Kiribati Dollar
    "KMF",  # Comorian Franc
    "KRW",  # South Korean Won
    "KWD",  # Kuwaiti Dinar
    "KYD",  # Cayman Islands Dollar
    "KZT",  # Kazakhstani Tenge
    "LAK",  # Laotian Kip
    "LBP",  # Lebanese Pound
    "LKR",  # Sri Lankan Rupee
    "LRD",  # Liberian Dollar
    "LSL",  # Lesotho Loti
    "LYD",  # Libyan Dinar
    "MAD",  # Moroccan Dirham
    "MDL",  # Moldovan Leu
    "MGA",  # Malagasy Ariary
    "MKD",  # Macedonian Denar
    "MMK",  # Myanma Kyat
    "MNT",  # Mongolian Tugrik
    "MOP",  # Macanese Pataca
    "MRU",  # Mauritanian Ouguiya
    "MUR",  # Mauritian Rupee
    "MVR",  # Maldivian Rufiyaa
    "MWK",  # Malawian Kwacha
    "MXN",  # Mexican Peso
    "MYR",  # Malaysian Ringgit
    "MZN",  # Mozambican Metical
    "NAD",  # Namibian Dollar
    "NGN",  # Nigerian Naira
    "NIO",  # Nicaraguan Córdoba
    "NOK",  # Norwegian Krone
    "NPR",  # Nepalese Rupee
    "NZD",  # New Zealand Dollar
    "OMR",  # Omani Rial
    "PAB",  # Panamanian Balboa
    "PEN",  # Peruvian Nuevo Sol
    "PGK",  # Papua New Guinean Kina
    "PHP",  # Philippine Peso
    "PKR",  # Pakistani Rupee
    "PLN",  # Polish Zloty
    "PYG",  # Paraguayan Guarani
    "QAR",  # Qatari Rial
    "RON",  # Romanian Leu
    "RSD",  # Serbian Dinar
    "RUB",  # Russian Ruble
    "RWF",  # Rwandan Franc
    "SAR",  # Saudi Riyal
    "SBD",  # Solomon Islands Dollar
    "SCR",  # Seychellois Rupee
    "SDG",  # Sudanese Pound
    "SEK",  # Swedish Krona
    "SGD",  # Singapore Dollar
    "SHP",  # Saint Helena Pound
    "SLL",  # Sierra Leonean Leone
    "SOS",  # Somali Shilling
    "SRD",  # Surinamese Dollar
    "SSP",  # South Sudanese Pound
    "STN",  # São Tomé and Príncipe Dobra
    "SYP",  # Syrian Pound
    "SZL",  # Swazi Lilangeni
    "THB",  # Thai Baht
    "TJS",  # Tajikistani Somoni
    "TMT",  # Turkmenistani Manat
    "TND",  # Tunisian Dinar
    "TOP",  # Tongan Paʻanga
    "TRY",  # Turkish Lira
    "TTD",  # Trinidad and Tobago Dollar
    "TVD",  # Tuvaluan Dollar
    "TWD",  # New Taiwan Dollar
    "TZS",  # Tanzanian Shilling
    "UAH",  # Ukrainian Hryvnia
    "UGX",  # Ugandan Shilling
    "USD",  # US Dollar
    "UYU",  # Uruguayan Peso
    "UZS",  # Uzbekistani Som
    "VEF",  # Venezuelan Bolívar Fuerte
    "VND",  # Vietnamese Dong
    "VUV",  # Vanuatu Vatu
    "WST",  # Samoan Tala
    "XAF",  # Central African CFA Franc
    "XAG",  # Silver Ounce
    "XAU",  # Gold Ounce
    "XCD",  # East Caribbean Dollar
    "XDR",  # Special Drawing Rights
    "XOF",  # West African CFA Franc
    "XPF",  # CFP Franc
    "YER",  # Yemeni Rial
    "ZAR",  # South African Rand
    "ZMW",  # Zambian Kwacha
    "ZWL",  # Zimbabwean Dollar
]





cities_in_india = [
    {"name": "Anantapur", "State": "Andhra Pradesh"},
    {"name": "Chittoor", "State": "Andhra Pradesh"},
    {"name": "East Godavari", "State": "Andhra Pradesh"},
    {"name": "Guntur", "State": "Andhra Pradesh"},
    {"name": "Krishna", "State": "Andhra Pradesh"},
    {"name": "Kurnool", "State": "Andhra Pradesh"},
    {"name": "Prakasam", "State": "Andhra Pradesh"},
    {"name": "Srikakulam", "State": "Andhra Pradesh"},
    {"name": "Sri Potti Sriramulu Nellore", "State": "Andhra Pradesh"},
    {"name": "Visakhapatnam", "State": "Andhra Pradesh"},
    {"name": "Vizianagaram", "State": "Andhra Pradesh"},
    {"name": "West Godavari", "State": "Andhra Pradesh"},
    {"name": "YSR Kadapa", "State": "Andhra Pradesh"},
    {"name": "Anjaw", "State": "Arunachal Pradesh"},
    {"name": "Changlang", "State": "Arunachal Pradesh"},
    {"name": "East Kameng", "State": "Arunachal Pradesh"},
    {"name": "East Siang", "State": "Arunachal Pradesh"},
    {"name": "Kra Daadi", "State": "Arunachal Pradesh"},
    {"name": "Kurung Kumey", "State": "Arunachal Pradesh"},
    {"name": "Lohit", "State": "Arunachal Pradesh"},
    {"name": "Longding", "State": "Arunachal Pradesh"},
    {"name": "Lower Dibang Valley", "State": "Arunachal Pradesh"},
    {"name": "Lower Siang", "State": "Arunachal Pradesh"},
    {"name": "Lower Subansiri", "State": "Arunachal Pradesh"},
    {"name": "Namsai", "State": "Arunachal Pradesh"},
    {"name": "Pakke Kessang", "State": "Arunachal Pradesh"},
    {"name": "Papum Pare", "State": "Arunachal Pradesh"},
    {"name": "Shi Yomi", "State": "Arunachal Pradesh"},
    {"name": "Siang", "State": "Arunachal Pradesh"},
    {"name": "Tawang", "State": "Arunachal Pradesh"},
    {"name": "Tirap", "State": "Arunachal Pradesh"},
    {"name": "Upper Dibang Valley", "State": "Arunachal Pradesh"},
    {"name": "Upper Siang", "State": "Arunachal Pradesh"},
    {"name": "Upper Subansiri", "State": "Arunachal Pradesh"},
    {"name": "West Kameng", "State": "Arunachal Pradesh"},
    {"name": "West Siang", "State": "Arunachal Pradesh"},
    {"name": "Baksa", "State": "Assam"},
    {"name": "Barpeta", "State": "Assam"},
    {"name": "Biswanath", "State": "Assam"},
    {"name": "Bongaigaon", "State": "Assam"},
    {"name": "Cachar", "State": "Assam"},
    {"name": "Charaideo", "State": "Assam"},
    {"name": "Chirang", "State": "Assam"},
    {"name": "Darrang", "State": "Assam"},
    {"name": "Dhemaji", "State": "Assam"},
    {"name": "Dhubri", "State": "Assam"},
    {"name": "Dibrugarh", "State": "Assam"},
    {"name": "Goalpara", "State": "Assam"},
    {"name": "Golaghat", "State": "Assam"},
    {"name": "Hailakandi", "State": "Assam"},
    {"name": "Hojai", "State": "Assam"},
    {"name": "Jorhat", "State": "Assam"},
    {"name": "Kamrup", "State": "Assam"},
    {"name": "Kamrup Metropolitan", "State": "Assam"},
    {"name": "Karbi Anglong", "State": "Assam"},
    {"name": "Karimganj", "State": "Assam"},
    {"name": "Kokrajhar", "State": "Assam"},
    {"name": "Lakhimpur", "State": "Assam"},
    {"name": "Majuli", "State": "Assam"},
    {"name": "Morigaon", "State": "Assam"},
    {"name": "Nagaon", "State": "Assam"},
    {"name": "Nalbari", "State": "Assam"},
    {"name": "Sivasagar", "State": "Assam"},
    {"name": "Sonitpur", "State": "Assam"},
    {"name": "South Salmara-Mankachar", "State": "Assam"},
    {"name": "Tinsukia", "State": "Assam"},
    {"name": "Udalguri", "State": "Assam"},
    {"name": "West Karbi Anglong", "State": "Assam"},
    {"name": "Araria", "State": "Bihar"},
    {"name": "Arwal", "State": "Bihar"},
    {"name": "Aurangabad", "State": "Bihar"},
    {"name": "Banka", "State": "Bihar"},
    {"name": "Begusarai", "State": "Bihar"},
    {"name": "Bhagalpur", "State": "Bihar"},
    {"name": "Bhojpur", "State": "Bihar"},
    {"name": "Buxar", "State": "Bihar"},
    {"name": "Darbhanga", "State": "Bihar"},
    {"name": "East Champaran", "State": "Bihar"},
    {"name": "Gaya", "State": "Bihar"},
    {"name": "Gopalganj", "State": "Bihar"},
    {"name": "Jamui", "State": "Bihar"},
    {"name": "Jehanabad", "State": "Bihar"},
    {"name": "Kaimur", "State": "Bihar"},
    {"name": "Katihar", "State": "Bihar"},
    {"name": "Khagaria", "State": "Bihar"},
    {"name": "Kishanganj", "State": "Bihar"},
    {"name": "Lakhisarai", "State": "Bihar"},
    {"name": "Madhepura", "State": "Bihar"},
    {"name": "Madhubani", "State": "Bihar"},
    {"name": "Munger", "State": "Bihar"},
    {"name": "Muzaffarpur", "State": "Bihar"},
    {"name": "Nalanda", "State": "Bihar"},
    {"name": "Nawada", "State": "Bihar"},
    {"name": "Patna", "State": "Bihar"},
    {"name": "Purnia", "State": "Bihar"},
    {"name": "Rohtas", "State": "Bihar"},
    {"name": "Saharsa", "State": "Bihar"},
    {"name": "Samastipur", "State": "Bihar"},
    {"name": "Saran", "State": "Bihar"},
    {"name": "Sheikhpura", "State": "Bihar"},
    {"name": "Sheohar", "State": "Bihar"},
    {"name": "Sitamarhi", "State": "Bihar"},
    {"name": "Siwan", "State": "Bihar"},
    {"name": "Supaul", "State": "Bihar"},
    {"name": "Vaishali", "State": "Bihar"},
    {"name": "West Champaran", "State": "Bihar"},
    {"name": "Balod", "State": "Chhattisgarh"},
    {"name": "Baloda Bazar", "State": "Chhattisgarh"},
    {"name": "Balrampur", "State": "Chhattisgarh"},
    {"name": "Bastar", "State": "Chhattisgarh"},
    {"name": "Bemetara", "State": "Chhattisgarh"},
    {"name": "Bijapur", "State": "Chhattisgarh"},
    {"name": "Bilaspur", "State": "Chhattisgarh"},
    {"name": "Dantewada", "State": "Chhattisgarh"},
    {"name": "Dhamtari", "State": "Chhattisgarh"},
    {"name": "Durg", "State": "Chhattisgarh"},
    {"name": "Gariaband", "State": "Chhattisgarh"},
    {"name": "Gaurela Pendra Marwahi", "State": "Chhattisgarh"},
    {"name": "Janjgir-Champa", "State": "Chhattisgarh"},
    {"name": "Jashpur", "State": "Chhattisgarh"},
    {"name": "Kabirdham", "State": "Chhattisgarh"},
    {"name": "Kanker", "State": "Chhattisgarh"},
    {"name": "Kondagaon", "State": "Chhattisgarh"},
    {"name": "Korba", "State": "Chhattisgarh"},
    {"name": "Koriya", "State": "Chhattisgarh"},
    {"name": "Mahasamund", "State": "Chhattisgarh"},
    {"name": "Mungeli", "State": "Chhattisgarh"},
    {"name": "Narayanpur", "State": "Chhattisgarh"},
    {"name": "Raigarh", "State": "Chhattisgarh"},
    {"name": "Raipur", "State": "Chhattisgarh"},
    {"name": "Rajnandgaon", "State": "Chhattisgarh"},
    {"name": "Sukma", "State": "Chhattisgarh"},
    {"name": "Surajpur", "State": "Chhattisgarh"},
    {"name": "Surguja", "State": "Chhattisgarh"},
    {"name": "North Goa", "State": "Goa"},
    {"name": "South Goa", "State": "Goa"},
    {"name": "Ahmedabad", "State": "Gujarat"},
    {"name": "Amreli", "State": "Gujarat"},
    {"name": "Anand", "State": "Gujarat"},
    {"name": "Aravalli", "State": "Gujarat"},
    {"name": "Banaskantha", "State": "Gujarat"},
    {"name": "Bharuch", "State": "Gujarat"},
    {"name": "Bhavnagar", "State": "Gujarat"},
    {"name": "Botad", "State": "Gujarat"},
    {"name": "Chhota Udaipur", "State": "Gujarat"},
    {"name": "Dahod", "State": "Gujarat"},
    {"name": "Dang", "State": "Gujarat"},
    {"name": "Devbhoomi Dwarka", "State": "Gujarat"},
    {"name": "Gandhinagar", "State": "Gujarat"},
    {"name": "Gir Somnath", "State": "Gujarat"},
    {"name": "Jamnagar", "State": "Gujarat"},
    {"name": "Junagadh", "State": "Gujarat"},
    {"name": "Kheda", "State": "Gujarat"},
    {"name": "Kutch", "State": "Gujarat"},
    {"name": "Mahisagar", "State": "Gujarat"},
    {"name": "Mehsana", "State": "Gujarat"},
    {"name": "Morbi", "State": "Gujarat"},
    {"name": "Narmada", "State": "Gujarat"},
    {"name": "Navsari", "State": "Gujarat"},
    {"name": "Panchmahal", "State": "Gujarat"},
    {"name": "Patan", "State": "Gujarat"},
    {"name": "Porbandar", "State": "Gujarat"},
    {"name": "Rajkot", "State": "Gujarat"},
    {"name": "Sabarkantha", "State": "Gujarat"},
    {"name": "Surat", "State": "Gujarat"},
    {"name": "Surendranagar", "State": "Gujarat"},
    {"name": "Tapi", "State": "Gujarat"},
    {"name": "Vadodara", "State": "Gujarat"},
    {"name": "Valsad", "State": "Gujarat"},
    {"name": "Ambala", "State": "Haryana"},
    {"name": "Bhiwani", "State": "Haryana"},
    {"name": "Charkhi Dadri", "State": "Haryana"},
    {"name": "Faridabad", "State": "Haryana"},
    {"name": "Fatehabad", "State": "Haryana"},
    {"name": "Gurugram", "State": "Haryana"},
    {"name": "Hisar", "State": "Haryana"},
    {"name": "Jhajjar", "State": "Haryana"},
    {"name": "Jind", "State": "Haryana"},
    {"name": "Kaithal", "State": "Haryana"},
    {"name": "Karnal", "State": "Haryana"},
    {"name": "Kurukshetra", "State": "Haryana"},
    {"name": "Mahendragarh", "State": "Haryana"},
    {"name": "Nuh", "State": "Haryana"},
    {"name": "Palwal", "State": "Haryana"},
    {"name": "Panchkula", "State": "Haryana"},
    {"name": "Panipat", "State": "Haryana"},
    {"name": "Rewari", "State": "Haryana"},
    {"name": "Rohtak", "State": "Haryana"},
    {"name": "Sirsa", "State": "Haryana"},
    {"name": "Sonipat", "State": "Haryana"},
    {"name": "Yamunanagar", "State": "Haryana"},
    {"name": "Bilaspur", "State": "Himachal Pradesh"},
    {"name": "Chamba", "State": "Himachal Pradesh"},
    {"name": "Hamirpur", "State": "Himachal Pradesh"},
    {"name": "Kangra", "State": "Himachal Pradesh"},
    {"name": "Kinnaur", "State": "Himachal Pradesh"},
    {"name": "Kullu", "State": "Himachal Pradesh"},
    {"name": "Lahaul and Spiti", "State": "Himachal Pradesh"},
    {"name": "Mandi", "State": "Himachal Pradesh"},
    {"name": "Shimla", "State": "Himachal Pradesh"},
    {"name": "Sirmaur", "State": "Himachal Pradesh"},
    {"name": "Solan", "State": "Himachal Pradesh"},
    {"name": "Una", "State": "Himachal Pradesh"},
    {"name": "Anantnag", "State": "Jammu and Kashmir"},
    {"name": "Bandipora", "State": "Jammu and Kashmir"},
    {"name": "Baramulla", "State": "Jammu and Kashmir"},
    {"name": "Budgam", "State": "Jammu and Kashmir"},
    {"name": "Doda", "State": "Jammu and Kashmir"},
    {"name": "Ganderbal", "State": "Jammu and Kashmir"},
    {"name": "Jammu", "State": "Jammu and Kashmir"},
    {"name": "Kathua", "State": "Jammu and Kashmir"},
    {"name": "Kishtwar", "State": "Jammu and Kashmir"},
    {"name": "Kulgam", "State": "Jammu and Kashmir"},
    {"name": "Kupwara", "State": "Jammu and Kashmir"},
    {"name": "Poonch", "State": "Jammu and Kashmir"},
    {"name": "Pulwama", "State": "Jammu and Kashmir"},
    {"name": "Rajouri", "State": "Jammu and Kashmir"},
    {"name": "Ramban", "State": "Jammu and Kashmir"},
    {"name": "Reasi", "State": "Jammu and Kashmir"},
    {"name": "Samba", "State": "Jammu and Kashmir"},
    {"name": "Shopian", "State": "Jammu and Kashmir"},
    {"name": "Srinagar", "State": "Jammu and Kashmir"},
    {"name": "Udhampur", "State": "Jammu and Kashmir"},
    {"name": "Bokaro", "State": "Jharkhand"},
    {"name": "Chatra", "State": "Jharkhand"},
    {"name": "Deoghar", "State": "Jharkhand"},
    {"name": "Dhanbad", "State": "Jharkhand"},
    {"name": "Dumka", "State": "Jharkhand"},
    {"name": "East Singhbhum", "State": "Jharkhand"},
    {"name": "Garhwa", "State": "Jharkhand"},
    {"name": "Giridih", "State": "Jharkhand"},
    {"name": "Godda", "State": "Jharkhand"},
    {"name": "Gumla", "State": "Jharkhand"},
    {"name": "Hazaribagh", "State": "Jharkhand"},
    {"name": "Jamtara", "State": "Jharkhand"},
    {"name": "Khunti", "State": "Jharkhand"},
    {"name": "Koderma", "State": "Jharkhand"},
    {"name": "Latehar", "State": "Jharkhand"},
    {"name": "Lohardaga", "State": "Jharkhand"},
    {"name": "Pakur", "State": "Jharkhand"},
    {"name": "Palamu", "State": "Jharkhand"},
    {"name": "Ramgarh", "State": "Jharkhand"},
    {"name": "Ranchi", "State": "Jharkhand"},
    {"name": "Sahebganj", "State": "Jharkhand"},
    {"name": "Seraikela Kharsawan", "State": "Jharkhand"},
    {"name": "Simdega", "State": "Jharkhand"},
    {"name": "West Singhbhum", "State": "Jharkhand"},
    {"name": "Bagalkot", "State": "Karnataka"},
    {"name": "Bangalore Rural", "State": "Karnataka"},
    {"name": "Bangalore Urban", "State": "Karnataka"},
    {"name": "Belgaum", "State": "Karnataka"},
    {"name": "Bellary", "State": "Karnataka"},
    {"name": "Bidar", "State": "Karnataka"},
    {"name": "Chamarajanagar", "State": "Karnataka"},
    {"name": "Chikkaballapur", "State": "Karnataka"},
    {"name": "Chikkamagaluru", "State": "Karnataka"},
    {"name": "Chitradurga", "State": "Karnataka"},
    {"name": "Dakshina Kannada", "State": "Karnataka"},
    {"name": "Davanagere", "State": "Karnataka"},
    {"name": "Dharwad", "State": "Karnataka"},
    {"name": "Gadag", "State": "Karnataka"},
    {"name": "Hassan", "State": "Karnataka"},
    {"name": "Haveri", "State": "Karnataka"},
    {"name": "Kalaburagi", "State": "Karnataka"},
    {"name": "Kodagu", "State": "Karnataka"},
    {"name": "Kolar", "State": "Karnataka"},
    {"name": "Koppal", "State": "Karnataka"},
    {"name": "Mandya", "State": "Karnataka"},
    {"name": "Mysore", "State": "Karnataka"},
    {"name": "Raichur", "State": "Karnataka"},
    {"name": "Ramanagara", "State": "Karnataka"},
    {"name": "Shimoga", "State": "Karnataka"},
    {"name": "Tumkur", "State": "Karnataka"},
    {"name": "Udupi", "State": "Karnataka"},
    {"name": "Uttara Kannada", "State": "Karnataka"},
    {"name": "Vijayapura", "State": "Karnataka"},
    {"name": "Yadgir", "State": "Karnataka"},
    {"name": "Alappuzha", "State": "Kerala"},
    {"name": "Ernakulam", "State": "Kerala"},
    {"name": "Idukki", "State": "Kerala"},
    {"name": "Kannur", "State": "Kerala"},
    {"name": "Kasaragod", "State": "Kerala"},
    {"name": "Kollam", "State": "Kerala"},
    {"name": "Kottayam", "State": "Kerala"},
    {"name": "Kozhikode", "State": "Kerala"},
    {"name": "Malappuram", "State": "Kerala"},
    {"name": "Palakkad", "State": "Kerala"},
    {"name": "Pathanamthitta", "State": "Kerala"},
    {"name": "Thiruvananthapuram", "State": "Kerala"},
    {"name": "Thrissur", "State": "Kerala"},
    {"name": "Wayanad", "State": "Kerala"},
    {"name": "Lakshadweep", "State": "Lakshadweep"},
    {"name": "Agar Malwa", "State": "Madhya Pradesh"},
    {"name": "Alirajpur", "State": "Madhya Pradesh"},
    {"name": "Anuppur", "State": "Madhya Pradesh"},
    {"name": "Ashoknagar", "State": "Madhya Pradesh"},
    {"name": "Balaghat", "State": "Madhya Pradesh"},
    {"name": "Barwani", "State": "Madhya Pradesh"},
    {"name": "Betul", "State": "Madhya Pradesh"},
    {"name": "Bhind", "State": "Madhya Pradesh"},
    {"name": "Bhopal", "State": "Madhya Pradesh"},
    {"name": "Burhanpur", "State": "Madhya Pradesh"},
    {"name": "Chachaura", "State": "Madhya Pradesh"},
    {"name": "Chhatarpur", "State": "Madhya Pradesh"},
    {"name": "Chhindwara", "State": "Madhya Pradesh"},
    {"name": "Damoh", "State": "Madhya Pradesh"},
    {"name": "Datia", "State": "Madhya Pradesh"},
    {"name": "Dewas", "State": "Madhya Pradesh"},
    {"name": "Dhar", "State": "Madhya Pradesh"},
    {"name": "Dindori", "State": "Madhya Pradesh"},
    {"name": "Guna", "State": "Madhya Pradesh"},
    {"name": "Gwalior", "State": "Madhya Pradesh"},
    {"name": "Harda", "State": "Madhya Pradesh"},
    {"name": "Hoshangabad", "State": "Madhya Pradesh"},
    {"name": "Indore", "State": "Madhya Pradesh"},
    {"name": "Jabalpur", "State": "Madhya Pradesh"},
    {"name": "Jhabua", "State": "Madhya Pradesh"},
    {"name": "Katni", "State": "Madhya Pradesh"},
    {"name": "Khandwa", "State": "Madhya Pradesh"},
    {"name": "Khargone", "State": "Madhya Pradesh"},
    {"name": "Maihar", "State": "Madhya Pradesh"},
    {"name": "Mandla", "State": "Madhya Pradesh"},
    {"name": "Mandsaur", "State": "Madhya Pradesh"},
    {"name": "Morena", "State": "Madhya Pradesh"},
    {"name": "Narsinghpur", "State": "Madhya Pradesh"},
    {"name": "Neemuch", "State": "Madhya Pradesh"},
    {"name": "Niwari", "State": "Madhya Pradesh"},
    {"name": "Panna", "State": "Madhya Pradesh"},
    {"name": "Raisen", "State": "Madhya Pradesh"},
    {"name": "Rajgarh", "State": "Madhya Pradesh"},
    {"name": "Ratlam", "State": "Madhya Pradesh"},
    {"name": "Rewa", "State": "Madhya Pradesh"},
    {"name": "Sagar", "State": "Madhya Pradesh"},
    {"name": "Satna", "State": "Madhya Pradesh"},
    {"name": "Sehore", "State": "Madhya Pradesh"},
    {"name": "Seoni", "State": "Madhya Pradesh"},
    {"name": "Shahdol", "State": "Madhya Pradesh"},
    {"name": "Shajapur", "State": "Madhya Pradesh"},
    {"name": "Sheopur", "State": "Madhya Pradesh"},
    {"name": "Shivpuri", "State": "Madhya Pradesh"},
    {"name": "Sidhi", "State": "Madhya Pradesh"},
    {"name": "Singrauli", "State": "Madhya Pradesh"},
    {"name": "Tikamgarh", "State": "Madhya Pradesh"},
    {"name": "Ujjain", "State": "Madhya Pradesh"},
    {"name": "Umaria", "State": "Madhya Pradesh"},
    {"name": "Vidisha", "State": "Madhya Pradesh"},
    {"name": "Ahmednagar", "State": "Maharashtra"},
    {"name": "Akola", "State": "Maharashtra"},
    {"name": "Amravati", "State": "Maharashtra"},
    {"name": "Aurangabad", "State": "Maharashtra"},
    {"name": "Beed", "State": "Maharashtra"},
    {"name": "Bhandara", "State": "Maharashtra"},
    {"name": "Buldhana", "State": "Maharashtra"},
    {"name": "Chandrapur", "State": "Maharashtra"},
    {"name": "Dhule", "State": "Maharashtra"},
    {"name": "Gadchiroli", "State": "Maharashtra"},
    {"name": "Gondia", "State": "Maharashtra"},
    {"name": "Hingoli", "State": "Maharashtra"},
    {"name": "Jalgaon", "State": "Maharashtra"},
    {"name": "Jalna", "State": "Maharashtra"},
    {"name": "Kolhapur", "State": "Maharashtra"},
    {"name": "Latur", "State": "Maharashtra"},
    {"name": "Mumbai City", "State": "Maharashtra"},
    {"name": "Mumbai Suburban", "State": "Maharashtra"},
    {"name": "Nagpur", "State": "Maharashtra"},
    {"name": "Nanded", "State": "Maharashtra"},
    {"name": "Nandurbar", "State": "Maharashtra"},
    {"name": "Nashik", "State": "Maharashtra"},
    {"name": "Osmanabad", "State": "Maharashtra"},
    {"name": "Palghar", "State": "Maharashtra"},
    {"name": "Parbhani", "State": "Maharashtra"},
    {"name": "Pune", "State": "Maharashtra"},
    {"name": "Raigad", "State": "Maharashtra"},
    {"name": "Ratnagiri", "State": "Maharashtra"},
    {"name": "Sangli", "State": "Maharashtra"},
    {"name": "Satara", "State": "Maharashtra"},
    {"name": "Sindhudurg", "State": "Maharashtra"},
    {"name": "Solapur", "State": "Maharashtra"},
    {"name": "Thane", "State": "Maharashtra"},
    {"name": "Wardha", "State": "Maharashtra"},
    {"name": "Washim", "State": "Maharashtra"},
    {"name": "Yavatmal", "State": "Maharashtra"},
    {"name": "Bishnupur", "State": "Manipur"},
    {"name": "Chandel", "State": "Manipur"},
    {"name": "Churachandpur", "State": "Manipur"},
    {"name": "Imphal East", "State": "Manipur"},
    {"name": "Imphal West", "State": "Manipur"},
    {"name": "Jiribam", "State": "Manipur"},
    {"name": "Kakching", "State": "Manipur"},
    {"name": "Kamjong", "State": "Manipur"},
    {"name": "Kangpokpi", "State": "Manipur"},
    {"name": "Noney", "State": "Manipur"},
    {"name": "Pherzawl", "State": "Manipur"},
    {"name": "Senapati", "State": "Manipur"},
    {"name": "Tamenglong", "State": "Manipur"},
    {"name": "Tengnoupal", "State": "Manipur"},
    {"name": "Thoubal", "State": "Manipur"},
    {"name": "Ukhrul", "State": "Manipur"},
    {"name": "East Garo Hills", "State": "Meghalaya"},
    {"name": "East Jaintia Hills", "State": "Meghalaya"},
    {"name": "East Khasi Hills", "State": "Meghalaya"},
    {"name": "North Garo Hills", "State": "Meghalaya"},
    {"name": "Ri Bhoi", "State": "Meghalaya"},
    {"name": "South Garo Hills", "State": "Meghalaya"},
    {"name": "South West Garo Hills", "State": "Meghalaya"},
    {"name": "South West Khasi Hills", "State": "Meghalaya"},
    {"name": "West Garo Hills", "State": "Meghalaya"},
    {"name": "West Jaintia Hills", "State": "Meghalaya"},
    {"name": "West Khasi Hills", "State": "Meghalaya"},
    {"name": "Aizawl", "State": "Mizoram"},
    {"name": "Champhai", "State": "Mizoram"},
    {"name": "Hnahthial", "State": "Mizoram"},
    {"name": "Khawzawl", "State": "Mizoram"},
    {"name": "Kolasib", "State": "Mizoram"},
    {"name": "Lawngtlai", "State": "Mizoram"},
    {"name": "Lunglei", "State": "Mizoram"},
    {"name": "Mamit", "State": "Mizoram"},
    {"name": "Saiha", "State": "Mizoram"},
    {"name": "Saitual", "State": "Mizoram"},
    {"name": "Serchhip", "State": "Mizoram"},
    {"name": "Dimapur", "State": "Nagaland"},
    {"name": "Kiphire", "State": "Nagaland"},
    {"name": "Kohima", "State": "Nagaland"},
    {"name": "Longleng", "State": "Nagaland"},
    {"name": "Mokokchung", "State": "Nagaland"},
    {"name": "Mon", "State": "Nagaland"},
    {"name": "Noklak", "State": "Nagaland"},
    {"name": "Peren", "State": "Nagaland"},
    {"name": "Phek", "State": "Nagaland"},
    {"name": "Tuensang", "State": "Nagaland"},
    {"name": "Wokha", "State": "Nagaland"},
    {"name": "Zunheboto", "State": "Nagaland"},
    {"name": "Angul", "State": "Odisha"},
    {"name": "Balangir", "State": "Odisha"},
    {"name": "Balasore", "State": "Odisha"},
    {"name": "Bargarh", "State": "Odisha"},
    {"name": "Bhadrak", "State": "Odisha"},
    {"name": "Boudh", "State": "Odisha"},
    {"name": "Cuttack", "State": "Odisha"},
    {"name": "Deogarh", "State": "Odisha"},
    {"name": "Dhenkanal", "State": "Odisha"},
    {"name": "Gajapati", "State": "Odisha"},
    {"name": "Ganjam", "State": "Odisha"},
    {"name": "Jagatsinghpur", "State": "Odisha"},
    {"name": "Jajpur", "State": "Odisha"},
    {"name": "Jharsuguda", "State": "Odisha"},
    {"name": "Kalahandi", "State": "Odisha"},
    {"name": "Kandhamal", "State": "Odisha"},
    {"name": "Kendrapara", "State": "Odisha"},
    {"name": "Kendujhar (Keonjhar)", "State": "Odisha"},
    {"name": "Khordha", "State": "Odisha"},
    {"name": "Koraput", "State": "Odisha"},
    {"name": "Malkangiri", "State": "Odisha"},
    {"name": "Mayurbhanj", "State": "Odisha"},
    {"name": "Nabarangpur", "State": "Odisha"},
    {"name": "Nayagarh", "State": "Odisha"},
    {"name": "Nuapada", "State": "Odisha"},
    {"name": "Puri", "State": "Odisha"},
    {"name": "Rayagada", "State": "Odisha"},
    {"name": "Sambalpur", "State": "Odisha"},
    {"name": "Subarnapur (Sonepur)", "State": "Odisha"},
    {"name": "Sundargarh", "State": "Odisha"},
    {"name": "Karaikal", "State": "Puducherry"},
    {"name": "Mahe", "State": "Puducherry"},
    {"name": "Puducherry", "State": "Puducherry"},
    {"name": "Yanam", "State": "Puducherry"},
    {"name": "Amritsar", "State": "Punjab"},
    {"name": "Barnala", "State": "Punjab"},
    {"name": "Bathinda", "State": "Punjab"},
    {"name": "Faridkot", "State": "Punjab"},
    {"name": "Fatehgarh Sahib", "State": "Punjab"},
    {"name": "Fazilka", "State": "Punjab"},
    {"name": "Ferozepur", "State": "Punjab"},
    {"name": "Gurdaspur", "State": "Punjab"},
    {"name": "Hoshiarpur", "State": "Punjab"},
    {"name": "Jalandhar", "State": "Punjab"},
    {"name": "Kapurthala", "State": "Punjab"},
    {"name": "Ludhiana", "State": "Punjab"},
    {"name": "Mansa", "State": "Punjab"},
    {"name": "Moga", "State": "Punjab"},
    {"name": "Muktsar", "State": "Punjab"},
    {"name": "Nawanshahr (Shahid Bhagat Singh Nagar)","State": "Punjab"},
    {"name": "Pathankot", "State": "Punjab"},
    {"name": "Patiala", "State": "Punjab"},
    {"name": "Rupnagar", "State": "Punjab"},
    {"name": "Sangrur", "State": "Punjab"},
    {"name": "SAS Nagar (Mohali)", "State": "Punjab"},
    {"name": "Tarn Taran", "State": "Punjab"},
    {"name": "Ajmer", "State": "Rajasthan"},
    {"name": "Alwar", "State": "Rajasthan"},
    {"name": "Banswara", "State": "Rajasthan"},
    {"name": "Baran", "State": "Rajasthan"},
    {"name": "Barmer", "State": "Rajasthan"},
    {"name": "Bharatpur", "State": "Rajasthan"},
    {"name": "Bhilwara", "State": "Rajasthan"},
    {"name": "Bikaner", "State": "Rajasthan"},
    {"name": "Bundi", "State": "Rajasthan"},
    {"name": "Chittorgarh", "State": "Rajasthan"},
    {"name": "Churu", "State": "Rajasthan"},
    {"name": "Dausa", "State": "Rajasthan"},
    {"name": "Dholpur", "State": "Rajasthan"},
    {"name": "Dungarpur", "State": "Rajasthan"},
    {"name": "Hanumangarh", "State": "Rajasthan"},
    {"name": "Jaipur", "State": "Rajasthan"},
    {"name": "Jaisalmer", "State": "Rajasthan"},
    {"name": "Jalore", "State": "Rajasthan"},
    {"name": "Jhalawar", "State": "Rajasthan"},
    {"name": "Jhunjhunu", "State": "Rajasthan"},
    {"name": "Jodhpur", "State": "Rajasthan"},
    {"name": "Karauli", "State": "Rajasthan"},
    {"name": "Kota", "State": "Rajasthan"},
    {"name": "Nagaur", "State": "Rajasthan"},
    {"name": "Pali", "State": "Rajasthan"},
    {"name": "Pratapgarh", "State": "Rajasthan"},
    {"name": "Rajsamand", "State": "Rajasthan"},
    {"name": "Sawai Madhopur", "State": "Rajasthan"},
    {"name": "Sikar", "State": "Rajasthan"},
    {"name": "Sirohi", "State": "Rajasthan"},
    {"name": "Sri Ganganagar", "State": "Rajasthan"},
    {"name": "Tonk", "State": "Rajasthan"},
    {"name": "Udaipur", "State": "Rajasthan"},
    {"name": "East Sikkim", "State": "Sikkim"},
    {"name": "North Sikkim", "State": "Sikkim"},
    {"name": "South Sikkim", "State": "Sikkim"},
    {"name": "West Sikkim", "State": "Sikkim"},
    {"name": "Ariyalur", "State": "Tamil Nadu"},
    {"name": "Chengalpattu", "State": "Tamil Nadu"},
    {"name": "Chennai", "State": "Tamil Nadu"},
    {"name": "Coimbatore", "State": "Tamil Nadu"},
    {"name": "Cuddalore", "State": "Tamil Nadu"},
    {"name": "Dharmapuri", "State": "Tamil Nadu"},
    {"name": "Dindigul", "State": "Tamil Nadu"},
    {"name": "Erode", "State": "Tamil Nadu"},
    {"name": "Kallakurichi", "State": "Tamil Nadu"},
    {"name": "Kanchipuram", "State": "Tamil Nadu"},
    {"name": "Kanyakumari", "State": "Tamil Nadu"},
    {"name": "Karur", "State": "Tamil Nadu"},
    {"name": "Krishnagiri", "State": "Tamil Nadu"},
    {"name": "Madurai", "State": "Tamil Nadu"},
    {"name": "Mayiladuthurai", "State": "Tamil Nadu"},
    {"name": "Nagapattinam", "State": "Tamil Nadu"},
    {"name": "Namakkal", "State": "Tamil Nadu"},
    {"name": "Nilgiris", "State": "Tamil Nadu"},
    {"name": "Perambalur", "State": "Tamil Nadu"},
    {"name": "Pudukkottai", "State": "Tamil Nadu"},
    {"name": "Ramanathapuram", "State": "Tamil Nadu"},
    {"name": "Ranipet", "State": "Tamil Nadu"},
    {"name": "Salem", "State": "Tamil Nadu"},
    {"name": "Sivaganga", "State": "Tamil Nadu"},
    {"name": "Tenkasi", "State": "Tamil Nadu"},
    {"name": "Thanjavur", "State": "Tamil Nadu"},
    {"name": "Theni", "State": "Tamil Nadu"},
    {"name": "Thoothukudi", "State": "Tamil Nadu"},
    {"name": "Tiruchirappalli", "State": "Tamil Nadu"},
    {"name": "Tirunelveli", "State": "Tamil Nadu"},
    {"name": "Tirupattur", "State": "Tamil Nadu"},
    {"name": "Tiruppur", "State": "Tamil Nadu"},
    {"name": "Tiruvallur", "State": "Tamil Nadu"},
    {"name": "Tiruvannamalai", "State": "Tamil Nadu"},
    {"name": "Tiruvarur", "State": "Tamil Nadu"},
    {"name": "Vellore", "State": "Tamil Nadu"},
    {"name": "Viluppuram", "State": "Tamil Nadu"},
    {"name": "Virudhunagar", "State": "Tamil Nadu"},
    {"name": "Adilabad", "State": "Telangana"},
    {"name": "Bhadradri Kothagudem", "State": "Telangana"},
    {"name": "Hyderabad", "State": "Telangana"},
    {"name": "Jagtial", "State": "Telangana"},
    {"name": "Jangaon", "State": "Telangana"},
    {"name": "Jayashankar Bhupalpally", "State": "Telangana"},
    {"name": "Jogulamba Gadwal", "State": "Telangana"},
    {"name": "Kamareddy", "State": "Telangana"},
    {"name": "Karimnagar", "State": "Telangana"},
    {"name": "Khammam", "State": "Telangana"},
    {"name": "Kumuram Bheem", "State": "Telangana"},
    {"name": "Mahabubabad", "State": "Telangana"},
    {"name": "Mahabubnagar", "State": "Telangana"},
    {"name": "Mancherial", "State": "Telangana"},
    {"name": "Medak", "State": "Telangana"},
    {"name": "Medchal-Malkajgiri", "State": "Telangana"},
    {"name": "Mulugu", "State": "Telangana"},
    {"name": "Nagarkurnool", "State": "Telangana"},
    {"name": "Nalgonda", "State": "Telangana"},
    {"name": "Narayanpet", "State": "Telangana"},
    {"name": "Nirmal", "State": "Telangana"},
    {"name": "Nizamabad", "State": "Telangana"},
    {"name": "Peddapalli", "State": "Telangana"},
    {"name": "Rajanna Sircilla", "State": "Telangana"},
    {"name": "Ranga Reddy", "State": "Telangana"},
    {"name": "Sangareddy", "State": "Telangana"},
    {"name": "Siddipet", "State": "Telangana"},
    {"name": "Suryapet", "State": "Telangana"},
    {"name": "Vikarabad", "State": "Telangana"},
    {"name": "Wanaparthy", "State": "Telangana"},
    {"name": "Warangal Rural", "State": "Telangana"},
    {"name": "Warangal Urban", "State": "Telangana"},
    {"name": "Yadadri Bhuvanagiri", "State": "Telangana"},
    {"name": "Dhalai", "State": "Tripura"},
    {"name": "Gomati", "State": "Tripura"},
    {"name": "Khowai", "State": "Tripura"},
    {"name": "North Tripura", "State": "Tripura"},
    {"name": "Sepahijala", "State": "Tripura"},
    {"name": "South Tripura", "State": "Tripura"},
    {"name": "Unakoti", "State": "Tripura"},
    {"name": "West Tripura", "State": "Tripura"},
    {"name": "Agra", "State": "Uttar Pradesh"},
    {"name": "Aligarh", "State": "Uttar Pradesh"},
    {"name": "Ambedkar Nagar", "State": "Uttar Pradesh"},
    {"name": "Amethi (Chatrapati Sahuji Mahraj Nagar)", "State": "Uttar Pradesh"},
    {"name": "Amroha (J.P. Nagar)", "State": "Uttar Pradesh"},
    {"name": "Auraiya", "State": "Uttar Pradesh"},
    {"name": "Ayodhya (Faizabad)", "State": "Uttar Pradesh"},
    {"name": "Azamgarh", "State": "Uttar Pradesh"},
    {"name": "Baghpat", "State": "Uttar Pradesh"},
    {"name": "Bahraich", "State": "Uttar Pradesh"},
    {"name": "Ballia", "State": "Uttar Pradesh"},
    {"name": "Balrampur", "State": "Uttar Pradesh"},
    {"name": "Banda", "State": "Uttar Pradesh"},
    {"name": "Barabanki", "State": "Uttar Pradesh"},
    {"name": "Bareilly", "State": "Uttar Pradesh"},
    {"name": "Basti", "State": "Uttar Pradesh"},
    {"name": "Bhadohi", "State": "Uttar Pradesh"},
    {"name": "Bijnor", "State": "Uttar Pradesh"},
    {"name": "Budaun", "State": "Uttar Pradesh"},
    {"name": "Bulandshahr", "State": "Uttar Pradesh"},
    {"name": "Chandauli", "State": "Uttar Pradesh"},
    {"name": "Chitrakoot", "State": "Uttar Pradesh"},
    {"name": "Deoria", "State": "Uttar Pradesh"},
    {"name": "Etah", "State": "Uttar Pradesh"},
    {"name": "Etawah", "State": "Uttar Pradesh"},
    {"name": "Farrukhabad", "State": "Uttar Pradesh"},
    {"name": "Fatehpur", "State": "Uttar Pradesh"},
    {"name": "Firozabad", "State": "Uttar Pradesh"},
    {"name": "Gautam Buddha Nagar", "State": "Uttar Pradesh"},
    {"name": "Ghaziabad", "State": "Uttar Pradesh"},
    {"name": "Ghazipur", "State": "Uttar Pradesh"},
    {"name": "Gonda", "State": "Uttar Pradesh"},
    {"name": "Gorakhpur", "State": "Uttar Pradesh"},
    {"name": "Hamirpur", "State": "Uttar Pradesh"},
    {"name": "Hapur (Panchsheel Nagar)", "State": "Uttar Pradesh"},
    {"name": "Hardoi", "State": "Uttar Pradesh"},
    {"name": "Hathras", "State": "Uttar Pradesh"},
    {"name": "Jalaun", "State": "Uttar Pradesh"},
    {"name": "Jaunpur", "State": "Uttar Pradesh"},
    {"name": "Jhansi", "State": "Uttar Pradesh"},
    {"name": "Kannauj", "State": "Uttar Pradesh"},
    {"name": "Kanpur Dehat", "State": "Uttar Pradesh"},
    {"name": "Kanpur Nagar", "State": "Uttar Pradesh"},
    {"name": "Kasganj (Kanshiram Nagar)", "State": "Uttar Pradesh"},
    {"name": "Kaushambi", "State": "Uttar Pradesh"},
    {"name": "Kushinagar (Padrauna)", "State": "Uttar Pradesh"},
    {"name": "Lakhimpur - Kheri", "State": "Uttar Pradesh"},
    {"name": "Lalitpur", "State": "Uttar Pradesh"},
    {"name": "Lucknow", "State": "Uttar Pradesh"},
    {"name": "Maharajganj", "State": "Uttar Pradesh"},
    {"name": "Mahoba", "State": "Uttar Pradesh"},
    {"name": "Mainpuri", "State": "Uttar Pradesh"},
    {"name": "Mathura", "State": "Uttar Pradesh"},
    {"name": "Mau", "State": "Uttar Pradesh"},
    {"name": "Meerut", "State": "Uttar Pradesh"},
    {"name": "Mirzapur", "State": "Uttar Pradesh"},
    {"name": "Moradabad", "State": "Uttar Pradesh"},
    {"name": "Muzaffarnagar", "State": "Uttar Pradesh"},
    {"name": "Pilibhit", "State": "Uttar Pradesh"},
    {"name": "Pratapgarh", "State": "Uttar Pradesh"},
    {"name": "Raebareli", "State": "Uttar Pradesh"},
    {"name": "Rampur", "State": "Uttar Pradesh"},
    {"name": "Saharanpur", "State": "Uttar Pradesh"},
    {"name": "Sambhal (Bhim Nagar)", "State": "Uttar Pradesh"},
    {"name": "Sant Kabir Nagar", "State": "Uttar Pradesh"},
    {"name": "Shahjahanpur", "State": "Uttar Pradesh"},
    {"name": "Shamali (Prabuddh Nagar)", "State": "Uttar Pradesh"},
    {"name": "Shravasti", "State": "Uttar Pradesh"},
    {"name": "Siddharthnagar", "State": "Uttar Pradesh"},
    {"name": "Sitapur", "State": "Uttar Pradesh"},
    {"name": "Sonbhadra", "State": "Uttar Pradesh"},
    {"name": "Sultanpur", "State": "Uttar Pradesh"},
    {"name": "Unnao", "State": "Uttar Pradesh"},
    {"name": "Varanasi", "State": "Uttar Pradesh"},
    {"name": "Almora", "State": "Uttarakhand"},
    {"name": "Bageshwar", "State": "Uttarakhand"},
    {"name": "Chamoli", "State": "Uttarakhand"},
    {"name": "Champawat", "State": "Uttarakhand"},
    {"name": "Dehradun", "State": "Uttarakhand"},
    {"name": "Haridwar", "State": "Uttarakhand"},
    {"name": "Nainital", "State": "Uttarakhand"},
    {"name": "Pauri Garhwal", "State": "Uttarakhand"},
    {"name": "Pithoragarh", "State": "Uttarakhand"},
    {"name": "Rudraprayag", "State": "Uttarakhand"},
    {"name": "Tehri Garhwal", "State": "Uttarakhand"},
    {"name": "Udham Singh Nagar", "State": "Uttarakhand"},
    {"name": "Uttarkashi", "State": "Uttarakhand"},
    {"name": "Alipurduar", "State": "West Bengal"},
    {"name": "Bankura", "State": "West Bengal"},
    {"name": "Birbhum", "State": "West Bengal"},
    {"name": "Cooch Behar", "State": "West Bengal"},
    {"name": "Dakshin Dinajpur (South Dinajpur)", "State": "West Bengal"},
    {"name": "Darjeeling", "State": "West Bengal"},
    {"name": "Hooghly", "State": "West Bengal"},
    {"name": "Howrah", "State": "West Bengal"},
    {"name": "Jalpaiguri", "State": "West Bengal"},
    {"name": "Jhargram", "State": "West Bengal"},
    {"name": "Kalimpong", "State": "West Bengal"},
    {"name": "Kolkata", "State": "West Bengal"},
    {"name": "Malda", "State": "West Bengal"},
    {"name": "Murshidabad", "State": "West Bengal"},
    {"name": "Nadia", "State": "West Bengal"},
    {"name": "North 24 Parganas", "State": "West Bengal"},
    {"name": "Paschim Bardhaman (West Bardhaman)", "State": "West Bengal"},
    {"name": "Paschim Medinipur (West Medinipur)", "State": "West Bengal"},
    {"name": "Purba Bardhaman (East Bardhaman)", "State": "West Bengal"},
    {"name": "Purba Medinipur (East Medinipur)", "State": "West Bengal"},
    {"name": "Purulia", "State": "West Bengal"},
    {"name": "South 24 Parganas", "State": "West Bengal"},
    {"name": "Uttar Dinajpur (North Dinajpur)", "State": "West Bengal"}
]





# contents.py

STATES_AND_CITIES = {

    'Andhra Pradesh': {
        'code': '28',
        'Gst_Code': 'IGST',
        'cities': [
    'Anakapalli',
    'Anantapur',
    'Bapatla',
    'Chittoor',
    'East Godavari',
    'Eluru',
    'Guntur',
    'Kadapa',
    'Kakinada',
    'Konaseema',
    'Krishna',
    'Kurnool',
    'Nandyal',
    'Nellore',
    'NTR',
    'Palnadu',
    'Parvathipuram Manyam',
    'Prakasam',
    'Srikakulam',
    'Sri Sathya Sai',
    'Tirupati',
    'Visakhapatnam',
    'Vizianagaram',
    'West Godavari',
    'Alluri Sitharama Raju',
    'Annamayya'
]


    },
    'Arunachal Pradesh': {
        'code': '12',
        'Gst_Code': 'IGST',
        'cities': [
    'Bichom',       
    'Tawang',
    'Itanagar Capital Complex',
    'West Kameng',
    'East Kameng',
    'Pakke Kessang',
    'Papum Pare',
    'Kurung Kumey',
    'Kra Daadi',
    'Lower Subansiri',
    'Upper Subansiri',
    'West Siang',
    'East Siang',
    'Siang',
    'Upper Siang',
    'Lower Siang',
    'Lepa Rada',
    'Shi Yomi',
    'Dibang Valley',
    'Lower Dibang Valley',
    'Anjaw',
    'Lohit',
    'Namsai',
    'Changlang',
    'Tirap',
    'Longding',
    'Kamle'
]

    },
    'Assam': {
        'code': '18',
        'Gst_Code': 'IGST',
        'cities': [
    'Baksa',
    'Barpeta',
    'Biswanath',
    'Bongaigaon',
    'Cachar',
    'Charaideo',
    'Chirang',
    'Darrang',
    'Dhemaji',
    'Dhubri',
    'Dibrugarh',
    'Goalpara',
    'Golaghat',
    'Hailakandi',
    'Hojai',
    'Jorhat',
    'Kamrup',
    'Kamrup Metropolitan',
    'Karbi Anglong',
    'Karimganj',
    'Kokrajhar',
    'Lakhimpur',
    'Majuli',
    'Morigaon',
    'Nagaon',
    'Nalbari',
    'Dima Hasao',
    'Sivasagar',
    'Sonitpur',
    'South Salmara-Mankachar',
    'Tinsukia',
    'Udalguri',
    'West Karbi Anglong'
]

    },
    'Bihar': {
        'code': '10',
        'Gst_Code': 'IGST',
        'cities': [
    'Araria',
    'Arwal',
    'Aurangabad',
    'Banka',
    'Begusarai',
    'Bhagalpur',
    'Bhojpur',
    'Buxar',
    'Darbhanga',
    'East Champaran',
    'Gaya',
    'Gopalganj',
    'Jamui',
    'Jehanabad',
    'Kaimur',
    'Katihar',
    'Khagaria',
    'Kishanganj',
    'Lakhisarai',
    'Madhepura',
    'Madhubani',
    'Munger',
    'Muzaffarpur',
    'Nalanda',
    'Nawada',
    'Patna',
    'Purnia',
    'Rohtas',
    'Saharsa',
    'Samastipur',
    'Saran',
    'Sheikhpura',
    'Sheohar',
    'Sitamarhi',
    'Siwan',
    'Supaul',
    'Vaishali',
    'West Champaran'
]

    },
   
    'Chhattisgarh': {
    'code': '22',
    'Gst_Code': 'IGST',
    'cities': [
    'Balod',
    'Baloda Bazar',
    'Bastar',
    'Bijapur',
    'Bilaspur',
    'Dantewada',
    'Dhamtari',
    'Durg',
    'Gariaband',
    'Janjgir-Champa',
    'Jashpur',
    'Kabirdham',
    'Kanker',
    'Korba',
    'Korea',
    'Mahasamund',
    'Mungeli',
    'Narayanpur',
    'Raigarh',
    'Raipur',
    'Rajnandgaon',
    'Sukma',
    'Surguja',
    'Surajpur',
    'Dantewada',
    'Dhamtari',
    'Durg',
    'Kabirdham'
]

    },
    'Goa': {
        'code': '30',
        'Gst_Code': 'IGST',
        'cities': [
            'North Goa',
            'South Goa'
        ]
    
    },
    'Gujarat': {
        'code': '24',
        'Gst_Code': 'IGST',
        'cities': [
            'Ahmedabad',
            'Amreli',
            'Anand',
            'Aravalli',
            'Banaskantha',
            'Bharuch',
            'Bhavnagar',
            'Dahod',
            'Dangs',
            'Gandhinagar',
            'Gir Somnath',
            'Jamnagar',
            'Junagadh',
            'Kachchh',
            'Kheda',
            'Mahisagar',
            'Mehsana',
            'Narmada',
            'Navsari',
            'Panchmahal',
            'Patan',
            'Patan',
            'Rajkot',
            'Sabarkantha',
            'Surat',
            'Surendranagar',
            'Tapi',
            'Vadodara',
            'Valsad'
        ]
    },
    'Haryana': {
        'code': '06',
        'Gst_Code': 'IGST',
        'cities': [
    'Ambala',
    'Bhiwani',
    'Charkhi Dadri',
    'Faridabad',
    'Fatehabad',
    'Gurugram',
    'Hisar',
    'Jhajjar',
    'Jind',
    'Kaithal',
    'Karnal',
    'Kurukshetra',
    'Mahendragarh',
    'Panchkula',
    'Pehowa',
    'Rewari',
    'Rohtak',
    'Sirsa',
    'Sonipat',
    'Yamunanagar',
    'Palwal',
    'Nuh'
]

    },
    'Himachal Pradesh': {
        'code': '02',
        'Gst_Code': 'IGST',
        'cities': [
    'Bilaspur',
    'Chamba',
    'Hamirpur',
    'Kinnaur',
    'Kullu',
    'Lahaul and Spiti',
    'Mandi',
    'Shimla',
    'Sirmaur',
    'Solan',
    'Una',
    'Nalagarh'
]

    },
    'Jammu and Kashmir': {
        'code': '01',
        'Gst_Code': 'UTGST',
        'cities': [
    'Anantnag',
    'Bandipora',
    'Baramulla',
    'Doda',
    'Ganderbal',
    'Jammu',
    'Kathua',
    'Kishtwar',
    'Kulgam',
    'Poonch',
    'Rajouri',
    'Ramban',
    'Reasi',
    'Samba',
    'Shopian',
    'Srinagar',
    'Udhampur',
    'Pulwama',
    'Kupwara',
    'Nowshera'
]

    },
    'Jharkhand': {
        'code': '20',
        'Gst_Code': 'IGST',
        'cities': [
    'Bokaro',
    'Chatra',
    'Deoghar',
    'Dhanbad',
    'Dumka',
    'East Singhbhum',
    'Garhwa',
    'Giridih',
    'Godda',
    'Gumla',
    'Hazaribagh',
    'Jamtara',
    'Khunti',
    'Koderma',
    'Latehar',
    'Lohardaga',
    'Pakur',
    'Palamu',
    'Ramgarh',
    'Ranchi',
    'Sahebganj',
    'Seraikela Kharsawan',
    'Simdega',
    'West Singhbhum'
]

    },
    'Karnataka': {
        'code': '29',
        'Gst_Code': 'IGST',
        'cities': [
    'Bagalkot',
    'Ballari',
    'Belagavi',
    'Bengaluru Rural',
    'Bengaluru Urban',
    'Bidar',
    'Chamarajanagar',
    'Chikballapur',
    'Chikkamagaluru',
    'Chitradurga',
    'Dakshina Kannada',
    'Davanagere',
    'Dharwad',
    'Gadag',
    'Hassan',
    'Haveri',
    'Kalaburagi',
    'Kodagu',
    'Kolar',
    'Koppal',
    'Mandya',
    'Mysuru',
    'Raichur',
    'Ramanagara',
    'Shivamogga',
    'Tumakuru',
    'Udupi',
    'Uttara Kannada',
    'Vijayanagara',
    'Vijayapura',
    'Yadgir'
]

    },
    'Kerala': {
        'code': '32',
        'Gst_Code': 'IGST',
        'cities': [
            'Alappuzha',
            'Ernakulam',
            'Idukki',
            'Kannur',
            'Kasaragod',
            'Kollam',
            'Kottayam',
            'Kozhikode',
            'Malappuram',
            'Palakkad',
            'Pathanamthitta',
            'Thiruvananthapuram',
            'Thrissur',
            'Wayanad'
        ]
    },
    'Madhya Pradesh': {
        'code': '23',
        'Gst_Code': 'IGST',
        'cities': [
    'Agar Malwa',
    'Alirajpur',
    'Anuppur',
    'Ashoknagar',
    'Balaghat',
    'Barwani',
    'Betul',
    'Bhind',
    'Bhopal',
    'Burhanpur',
    'Chhatarpur',
    'Chhindwara',
    'Damoh',
    'Datia',
    'Dewas',
    'Dhar',
    'Dindori',
    'Guna',
    'Gwalior',
    'Harda',
    'Hoshangabad',
    'Indore',
    'Jabalpur',
    'Jhabua',
    'Katni',
    'Khandwa',
    'Khargone',
    'Mandla',
    'Mandsaur',
    'Morena',
    'Narsinghpur',
    'Neemuch',
    'Niwari',
    'Panna',
    'Raisen',
    'Rajgarh',
    'Ratlam',
    'Rewa',
    'Sagar',
    'Satna',
    'Sehore',
    'Seoni',
    'Shahdol',
    'Shajapur',
    'Sheopur',
    'Shivpuri',
    'Sidhi',
    'Singrauli',
    'Tikamgarh',
    'Ujjain',
    'Umaria',
    'Vidisha'
]

    },
    'Maharashtra': {
        'code': '27',
        'Gst_Code': 'CGST+IGST',
        'cities': [
    'Ahmednagar',
    'Akola',
    'Amravati',
    'Aurangabad',
    'Beed',
    'Bhandara',
    'Buldhana',
    'Chandrapur',
    'Dhule',
    'Gadchiroli',
    'Gondia',
    'Hingoli',
    'Jalgaon',
    'Jalna',
    'Kolhapur',
    'Latur',
    'Mumbai City',
    'Mumbai Suburban',
    'Nagpur',
    'Nanded',
    'Nandurbar',
    'Nashik',
    'Osmanabad',
    'Palghar',
    'Parbhani',
    'Pune',
    'Raigad',
    'Ratnagiri',
    'Sangli',
    'Satara',
    'Sindhudurg',
    'Solapur',
    'Thane',
    'Wardha',
    'Washim',
    'Yavatmal'
]

    },
    'Manipur': {
        'code': '14',
        'Gst_Code': 'IGST',
        'cities': [
    'Bishnupur',
    'Chandel',
    'Churachandpur',
    'Imphal East',
    'Imphal West',
    'Jiribam',
    'Kakching',
    'Kamjong',
    'Kangpokpi',
    'Noney',
    'Pherzawl',
    'Senapati',
    'Tamenglong',
    'Tengnoupal',
    'Thoubal',
    'Ukhrul'
]

    },
    'Meghalaya': {
        'code': '17',
        'Gst_Code': 'IGST',
        'cities': [
    'East Garo Hills',
    'East Khasi Hills',
    'Jaintia Hills',
    'North Garo Hills',
    'Ri Bhoi',
    'South Garo Hills',
    'South West Garo Hills',
    'South West Khasi Hills',
    'West Garo Hills',
    'West Khasi Hills',
    'West Jaintia Hills'
]

    },
    'Mizoram': {
        'code': '15',
        'Gst_Code': 'IGST',
        'cities': [
    'Aizawl',
    'Champhai',
    'Hnahthial',
    'Lunglei',
    'Mamit',
    'Saiha',
    'Saitual',
    'Serchhip',
    'Kolasib',
    'Lawngtlai',
    'Lunglei'
]

    },
    'Nagaland': {
        'code': '13',
        'Gst_Code': 'IGST',
        'cities': [
    'Dimapur',
    'Kiphire',
    'Kohima',
    'Longleng',
    'Mokokchung',
    'Mon',
    'Peren',
    'Phek',
    'Tuensang',
    'Wokha',
    'Zunheboto',
    'Zunheboto',
    'Peren',
    'Phek',
    'Mokokchung',
    'Kohima'
]

    },
    'Odisha': {
        'code': '21',
        'Gst_Code': 'IGST',
        'cities': [
    'Angul',
    'Balangir',
    'Balasore',
    'Bargarh',
    'Bhadrak',
    'Boudh',
    'Cuttack',
    'Deogarh',
    'Dhenkanal',
    'Gajapati',
    'Ganjam',
    'Jagatsinghpur',
    'Jajpur',
    'Jharsuguda',
    'Kalahandi',
    'Kandhamal',
    'Kendrapara',
    'Keonjhar',
    'Khordha',
    'Koraput',
    'Malkangiri',
    'Mayurbhanj',
    'Nabarangpur',
    'Nayagarh',
    'Nuapada',
    'Puri',
    'Rayagada',
    'Sambalpur',
    'Subarnapur',
    'Sundargarh'
]

    },
    'Punjab': {
        'code': '03',
        'Gst_Code': 'IGST',
        'cities': [
    'Amritsar',
    'Barnala',
    'Bathinda',
    'Faridkot',
    'Fatehgarh Sahib',
    'Fazilka',
    'Gurdaspur',
    'Hoshiarpur',
    'Jalandhar',
    'Kapurthala',
    'Ludhiana',
    'Mansa',
    'Moga',
    'Pathankot',
    'Patiala',
    'Rupnagar',
    'S.a.s. Nagar (Mohali)',
    'Sangrur',
    'Shaheed Bhagat Singh Nagar',
    'Tarn Taran',
    'Sri Muktsar Sahib',
    'Nawanshahr',
    'Malerkotla'
]

    },
    'Rajasthan': {
        'code': '08',
        'Gst_Code': 'IGST',
        'cities': [
    'Ajmer',
    'Alwar',
    'Banswara',
    'Baran',
    'Barmer',
    'Bikaner',
    'Bundi',
    'Churu',
    'Dausa',
    'Dholpur',
    'Dungarpur',
    'Ganganagar',
    'Hanumangarh',
    'Jaipur',
    'Jaisalmer',
    'Jalore',
    'Jodhpur',
    'Kota',
    'Nagaur',
    'Pali',
    'Rajsamand',
    'Sawai Madhopur',
    'Sikar',
    'Tonk',
    'Udaipur',
    'Banswara',
    'Ajmer',
    'Alwar',
    'Barmer',
    'Bikaner',
    'Churu',
    'Dholpur'
]

    },
    'Sikkim': {
        'code': '11',
        'Gst_Code': 'IGST',
        'cities': [
    'East Sikkim',
    'North Sikkim',
    'South Sikkim',
    'West Sikkim',
    'Gangtok'
]

    },
    'Tamil Nadu': {
        'code': '33',
        'Gst_Code': 'IGST',
        'cities': [
    'Ariyalur',
    'Chennai',
    'Chengalpattu',
    'Dharmapuri',
    'Dindigul',
    'Erode',
    'Kanchipuram',
    'Kanyakumari',
    'Karur',
    'Krishnagiri',
    'Madurai',
    'Nagapattinam',
    'Namakkal',
    'Nilgiris',
    'Perambalur',
    'Pudukkottai',
    'Ramanathapuram',
    'Salem',
    'Sivaganga',
    'Thanjavur',
    'Theni',
    'Tiruchirappalli',
    'Tirunelveli',
    'Tiruppur',
    'Tiruvallur',
    'Tiruvannamalai',
    'Vellore',
    'Villupuram',
    'Virudhunagar',
    'Ariyalur',
    'Chennai',
    'Chengalpattu',
    'Dharmapuri',
    'Dindigul',
    'Erode',
    'Kanchipuram',
    'Kanyakumari',
    'Karur'
]

    },
    'Telangana': {
        'code': '36',
        'Gst_Code': 'IGST',
        'cities': [
    'Adilabad',
    'Hyderabad',
    'Jagtiyal',
    'Jangaon',
    'Jayashankar Bhupalpally',
    'Jogulamba Gadwal',
    'Kamareddy',
    'Karimnagar',
    'Khammam',
    'Komaram Bheem Asifabad',
    'Mahabubnagar',
    'Mancherial',
    'Medak',
    'Medchal-Malkajgiri',
    'Nalgonda',
    'Nizamabad',
    'Peddapalli',
    'Rajanna Sircilla',
    'Ranga Reddy',
    'Sangareddy',
    'Siddipet',
    'Suryapet',
    'Vikarabad',
    'Warangal Rural',
    'Warangal Urban',
    'Yadadri Bhuvanagiri',
    'Nagarkurnool',
    'Wanaparthy',
    'Mahabubnagar',
    'Khammam',
    'Rajanna Sircilla',
    'Sangareddy',
    'Warangal Urban'
]

    },
    'Tripura': {
        'code': '16',
        'Gst_Code': 'IGST',
        'cities': [
            'Dhalai',
            'Khowai',
            'North Tripura',
            'Sepahijala',
            'South Tripura',
            'Unakoti',
            'West Tripura'
        ]
    },
    'Uttar Pradesh': {
        'code': '09',
        'Gst_Code': 'IGST',
        'cities': [
            'Agra',
            'Aligarh',
            'Ambedkar Nagar',
            'Amethi',
            'Amroha',
            'Auraiya',
            'Ayodhya',
            'Azamgarh',
            'Baghpat',
            'Bahraich',
            'Ballia',
            'Balrampur',
            'Banda',
            'Barabanki',
            'Bareilly',
            'Basti',
            'Bhadohi',
            'Bijnor',
            'Budaun',
            'Bulandshahr',
            'Chandauli',
            'Chitrakoot',
            'Deoria',
            'Etah',
            'Etawah',
            'Farrukhabad',
            'Fatehpur',
            'Firozabad',
            'Gautam Buddha Nagar',
            'Ghaziabad',
            'Ghazipur',
            'Gonda',
            'Gorakhpur',
            'Hamirpur',
            'Hapur',
            'Hardoi',
            'Hathras',
            'Jalaun',
            'Jaunpur',
            'Jhansi',
            'Kannauj',
            'Kanpur Dehat',
            'Kanpur Nagar',
            'Kasganj',
            'Kaushambi',
            'Kushinagar',
            'Lakhimpur Kheri',
            'Lalitpur',
            'Lucknow',
            'Maharajganj',
            'Mahoba',
            'Mainpuri',
            'Mathura',
            'Mau',
            'Meerut',
            'Mirzapur',
            'Moradabad',
            'Muzaffarnagar',
            'Pilibhit',
            'Pratapgarh',
            'Prayagraj',
            'Raebareli',
            'Rampur',
            'Saharanpur',
            'Sambhal',
            'Sant Kabir Nagar',
            'Shahjahanpur',
            'Shamli',
            'Shrawasti',
            'Siddharthnagar',
            'Sitapur',
            'Sonbhadra',
            'Sultanpur',
            'Unnao',
            'Varanasi'
        ]
    },
    'Uttarakhand': {
        'code': '05',
        'Gst_Code': 'IGST',
        'cities': [
            'Almora',
            'Bageshwar',
            'Champawat',
            'Dehradun',
            'Haridwar',
            'Nainital',
            'Pauri Garhwal',
            'Pithoragarh',
            'Rudraprayag',
            'Tehri Garhwal',
            'Udham Singh Nagar',
            'Uttarkashi'
        ]
    },
    'West Bengal': {
        'code': '19',
        'Gst_Code': 'IGST',
        'cities': [
            'Bankura',
            'Bardhaman',
            'Birbhum',
            'Burdwan',
            'Cooch Behar',
            'Dakshin Dinajpur',
            'Darjeeling',
            'Hooghly',
            'Howrah',
            'Jalpaiguri',
            'Jhargram',
            'Kolkata',
            'Malda',
            'Murshidabad',
            'Nadia',
            'North 24 Parganas',
            'South 24 Parganas',
            'Purulia',
            'Uttar Dinajpur'
        ]
    },
    'Andaman and Nicobar Islands': {
        'code': '35',
        'Gst_Code': 'UTGST',
        'cities': [
            'Andaman and Nicobar Islands'
        ]
    },
    'Chandigarh': {
        'code': '04',
        'Gst_Code': 'UTGST',
        'cities': [
            'Chandigarh'
        ]
    },
    'Dadra and Nagar Haveli and Daman and Diu': {
        'code': '26',
        'Gst_Code': 'UTGST',
        'cities': [
            'Dadra and Nagar Haveli',
            'Daman',
            'Diu'
        ]
    },
    'Lakshadweep': {
        'code': '31',
        'Gst_Code': 'UTGST',
        'cities': [
            'Lakshadweep'
        ]
    },
    'Delhi': {
        'code': '07',
        'Gst_Code': 'UTGST',
        'cities': [
            'Delhi'
        ]
    },
    'Puducherry': {
        'code': '34',
        'Gst_Code': 'UTGST',
        'cities': [
            'Karaikal',
            'Mahe',
            'Puducherry',
            'Yanam'
        ]
    },
    'Ladakh': {
        'code': '38',
        'Gst_Code': 'UTGST',
        'cities': [
            'Leh',
            'Kargil'
        ]
    }
}





    # Add more states and cities here




# Supplier_Customer_Masters:- GST TAX CODE
# data.py (or directly in views.py)

GST_STATE_CODES = {
    '27': 'CGST+IGST',  # Maharashtra
    '37': 'IGST',  # Andhra Pradesh
    '12': 'IGST',  # Arunachal Pradesh
    '18': 'IGST',  # Assam
    '10': 'IGST',  # Bihar
    '22': 'IGST',  # Chhattisgarh
    '30': 'IGST',  # Goa
    '24': 'IGST',  # Gujarat
    '06': 'IGST',  # Haryana
    '02': 'IGST',  # Himachal Pradesh
    '20': 'IGST',  # Jharkhand
    '29': 'IGST',  # Karnataka
    '32': 'IGST',  # Kerala
    '23': 'IGST',  # Madhya Pradesh
    '14': 'IGST',  # Manipur
    '17': 'IGST',  # Meghalaya
    '15': 'IGST',  # Mizoram
    '13': 'IGST',  # Nagaland
    '21': 'IGST',  # Odisha
    '03': 'IGST',  # Punjab
    '08': 'IGST',  # Rajasthan
    '11': 'IGST',  # Sikkim
    '33': 'IGST',  # Tamil Nadu
    '36': 'IGST',  # Telangana
    '16': 'IGST',  # Tripura
    '09': 'IGST',  # Uttar Pradesh
    '05': 'IGST',  # Uttarakhand
    '19': 'IGST',  # West Bengal
    # Union Territories
    '35': 'UTGST',  # Andaman and Nicobar Islands
    '04': 'UTGST',  # Chandigarh
    '26': 'UTGST',  # Dadra and Nagar Haveli and Daman and Diu
    '31': 'UTGST',  # Lakshadweep
    '07': 'UTGST',  # Delhi
    '34': 'UTGST',  # Puducherry
    '38': 'UTGST',  # Ladakh
    '01': 'UTGST',  # Jammu and Kashmir
}
