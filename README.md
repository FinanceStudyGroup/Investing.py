# Investing.py
This is a webscraper for downloading price and yield data currently unavailable in R.
Data are being collected from Investing.com, using the Selenium package for Python.

-----------------------------------------------------------------------------------------------------------------
In corporate valuation, we take as our input data measures of profitability that come from the accounting of
the companies considered, and measures of risk and price that come from the stock market.

Specifically, in valuing a given company by DCF, we need a measure of the cash flows the company will likely generate
into the future, and a measure of the macroeconomic risk inherent in this company.

In order to determine the likely cash-flow-generative ability of the company, we can examine the company's
unlevered free cash flow, a special derived item that we can determine from the accounting.

However, in assessing risk things can become complicated. In order to do this we would need the beta
of this company, the market rate of return, risk free rate, and the equity risk premium. 
In DCF these data then allow us to determine the cost of equity capital for the given asset,
leaving only then the cost of debt, and possibly preferred stock, to be determined.

These data are derived from price, the yield to maturity on assumed riskless government bonds, and
estimates of the expected earnings on market representative equities.

Without price and yield data, all our efforts in valuation can be stopped dead in their tracks.

To facilitate this process, we've built the following webscraper for collecting price and yield data
currently inaccessible in R. While in the future, new packages may be brought out allowing more immediate
access to these data, it's important to be able to break down this workflow into its essential steps,
and automate those, so that we can maintain access to the data in the event that the APIs behind R's
capabilities may change.

-----------------------------------------------------------------------------------------------------------------


To run this program, be sure to get [Selenium](https://www.seleniumhq.org/), and the most recent releases of [Google Chrome](https://www.google.com/chrome/?brand=CHBF&utm_source=bing&utm_medium=cpc&utm_campaign=1005992%20%7C%20Chrome%20Win10%20%7C%20DR%20%7C%20ESS01%20%7C%20NA%20%7C%20US%20%7C%20en%20%7C%20Desk%20%7C%20BING%20SEM%20%7C%20BKWS%20~%20Top%20KWDS%20-%20Exact&utm_term=google%20chrome&utm_content=Google%20Chrome%20-%20Exact&ds_kid=43700010220923516&gclid=CNupzfPj--ACFduGxQIdWPcHaA&gclsrc=ds),
and [Chrome Driver](https://chromedriver.storage.googleapis.com/index.html?path=2.46/).

The Selenium package for Python allows for automation of an instance of the web browser.
In this way, we can automate the tedious processes behind data collection.

From the command line, we can simply run,

```
python Investing.py
```
after which, we will be prompted for the following data for Investing.com, and parameters for the function,

1. Email address for Investing.com
2. Password for Investing.com
3. Mode (Investing.py takes as an argument, one of 75 different modes for collecting different data)
4. Interval (the data collection interval)
5. Destination folder

As an example, you might input the following,

Mode:
```
US
```

Interval:
```
10
```

and as for destination folder, you might copy the path to the folder on your local machine where you intend to store the data.

In running this download, we can collect the full yield curve on US government bonds across a 10-year interval of time,
leading up to the present date. Not only does this give us immediate access to measures of the risk free rate,
we can examine in Python or R how these rates may have changed over a recent historical interval.

With the 75 modes of this function, we can collect all yield data available from Investing.com, as well as index
prices and a given watchlist of equities, for use in risk analysis and valuation.

Any of the modes provided can easily be modified within Python, but our aim was to provide the broadest possible set of
coverage for the likely range of use cases within the valuation and investment research workflow.

-----------------------------------------------------------------------------------------------------------------
# Modes
Function modes are based on the International Organization for Standardization's ISO 3166-1 standard (specifically alpha-2,
and alpha-3), two- and three-digit alphabetical codes for denoting the names of countries.
Using these codes, we have defined a set of different modes for downloading various pieces of data from Investing.com.
These modes are listed below.

By providing the alpha-2 code for the mode of the function, we can download bond yields on for the given country,
formatted according to the alpha-3 code.

Additional modes include, "Watchlist," "Indices," "ETF," and "Bonds," where the "Bonds" mode provides the available set of 
1-, 5-, and 10-year yields on the set of countries having those maturities in common.

-----------------------------------------------------------------------------------------------------------------

| Alpha-2 | Alpha-3 | Country                                              |
|---------|---------|------------------------------------------------------|
| AR      | ARG     | Argentina                                            |
| AU      | AUS     | Australia                                            |
| AT      | AUT     | Austria                                              |
| BH      | BHR     | Bahrain                                              |
| BD      | BGD     | Bangladesh                                           |
| BE      | BEL     | Belgium                                              |
| BW      | BWA     | Botswana                                             |
| BR      | BRA     | Brazil                                               |
| BG      | BGR     | Bulgaria                                             |
| CA      | CAN     | Canada                                               |
| CL      | CHL     | Chile                                                |
| CN      | CHN     | China                                                |
| CO      | COL     | Colombia                                             |
| HR      | HRV     | Croatia                                              |
| CZ      | CZE     | Czechia                                              |
| DK      | DNK     | Denmark                                              |
| EG      | EGY     | Egypt                                                |
| FI      | FIN     | Finland                                              |
| FR      | FRA     | France                                               |
| DE      | DEU     | Germany                                              |
| GR      | GRC     | Greece                                               |
| HK      | HKG     | Hong Kong                                            |
| HU      | HUN     | Hungary                                              |
| IS      | ISL     | Iceland                                              |
| IN      | IND     | India                                                |
| ID      | IDN     | Indonesia                                            |
| IE      | IRL     | Ireland                                              |
| IL      | ISR     | Israel                                               |
| IT      | ITA     | Italy                                                |
| JP      | JPN     | Japan                                                |
| JO      | JOR     | Jordan                                               |
| KE      | KEN     | Kenya                                                |
| LV      | LVA     | Latvia                                               |
| LT      | LTU     | Lithuania                                            |
| MY      | MYS     | Malaysia                                             |
| MT      | MLT     | Malta                                                |
| MU      | MUS     | Mauritius                                            |
| MX      | MEX     | Mexico                                               |
| MA      | MAR     | Morocco                                              |
| NA      | NAM     | Namibia                                              |
| NL      | NLD     | Netherlands                                          |
| NZ      | NZL     | New Zealand                                          |
| NG      | NGA     | Nigeria                                              |
| NO      | NOR     | Norway                                               |
| PK      | PAK     | Pakistan                                             |
| PE      | PER     | Peru                                                 |
| PH      | PHL     | Philippines                                          |
| PL      | POL     | Poland                                               |
| PT      | PRT     | Portugal                                             |
| QA      | QAT     | Qatar                                                |
| RO      | ROU     | Romania                                              |
| RU      | RUS     | Russian Federation                                   |
| RS      | SRB     | Serbia                                               |
| SG      | SGP     | Singapore                                            |
| SK      | SVK     | Slovakia                                             |
| SI      | SVN     | Slovenia                                             |
| ZA      | ZAF     | South Africa                                         |
| KR      | KOR     | Korea, Republic of                                   |
| ES      | ESP     | Spain                                                |
| LK      | LKA     | Sri Lanka                                            |
| SE      | SWE     | Sweden                                               |
| CH      | CHE     | Switzerland                                          |
| TW      | TWN     | Taiwan, Province of China                            |
| TH      | THA     | Thailand                                             |
| TR      | TUR     | Turkey                                               |
| UG      | UGA     | Uganda                                               |
| UA      | UKR     | Ukraine                                              |
| GB      | GBR     | United Kingdom of Great Britain and Northern Ireland |
| US      | USA     | United States of America                             |
| VE      | VEN     | Venezuela, Bolivarian Republic of                    |
| VN      | VNM     | Viet Nam                                             |
