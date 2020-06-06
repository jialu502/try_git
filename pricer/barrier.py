import numpy as np
import pandas as pd 
class Barrier():

    cp:  "call or put"
    ul:  "underlying price"
    sp:  "strike price"
    dte: "days to expiry (in days)"
    ir:  "inerest rates"
    iv : "impled volatility"
    diy: "days in year"

    def __init__(self, ul , data_path):
        self.ul = ul
        self.upper_barrier_level = ul *  1.03
        self.lower_barrier_level = ul * 0.70
        self.coupon_rate = 0.31
        self.strike_price = ul * 1.00
        self.valuation_date = pd.Timestamp("2019-01-03")
        self.start_date = pd.Timestamp("2019-01-04")
        self.end_date = pd.Timestamp("2019-12-27")
        self.data = self.get_data(data_path)
        self.get_monitoring_dates()
        return
        
    def get_data(self, path):
        df = pd.read_excel(path, sheet_name = "Sheet1")
        df.columns  = ["date","price"]
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace = True)
        df = df.loc[self.valuation_date:self.end_date]
        return df

    def get_monitoring_dates(self):
        monitoring_dates  = ["2019-02-01",
                    "2019-03-04",
                    "2019-03-29",
                    "2019-04-26",
                    "2019-05-31",
                    "2019-06-28",
                    "2019-07-26",
                    "2019-08-23",
                    "2019-09-20",
                    "2019-10-25",
                    "2019-11-22",
                    "2019-12-27"]
        self.monitoring_dates = [pd.Timestamp(x) for x in monitoring_dates]
        return
    def geometric_brownian_motion(self, ul, iv ,  ir , dte , diy , nobs) -> "ndarray. row = t, columns = paths":
        dt = 1 / diy

        # Initialize the array
        S = np.zeros((dte + 1, nobs))    
        S[0] = ul

        # Discount 
        df = np.exp(-ir * dt)

        for t in range(1, dte + 1):
            S[t] = S[t - 1] * np.exp((ir - 0.5 * iv ** 2) * dt + iv * np.sqrt(dt) * np.random.standard_normal(nobs))
        return S

