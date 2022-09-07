import pandas as pd
from datetime import datetime
import os
import re
import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action = "ignore", category = FutureWarning)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if not os.path.exists("speicher/students.csv"):

    studentdf = pd.read_excel("speicher\\students.xlsx")

    studentdf["gewaehlt"] = False
    studentdf.to_csv("speicher/students.csv", index=False)


def receive_input(undo=False):
    if not undo:
        student = input("Bitte Schülerausweis vorhalten oder Namen eingeben: ")
    else:
        student = input("UNDO - Bitte Schülerausweis vorhalten oder Namen eingeben: ")
    return student.strip()

def get_dataframe_row_from_id(id, df):
    mask = df["Ausweisnummer"] == int(id)
    return mask

def get_dataframe_rows_from_name(name, df):
    mask = df["Name"].str.contains(rf"(?<![äöüÄÖÜß\w]){name}", flags= re.I, regex=True)
    return mask


def undo(df):

    while True:
        student = receive_input(undo=True)


        if student == "redo":
            return df


        if student.isdigit():
            mask = get_dataframe_row_from_id(id=student, df=df)
            if df[mask].shape[0] == 1:
                if df.loc[mask, "gewaehlt"].bool():
                    df.loc[mask, "gewaehlt"] = False
                    print(bcolors.OKGREEN + f"{df.loc[mask, 'Name'].values[0]} darf wieder wählen" + bcolors.ENDC)
                    return df
                else:
                    print(bcolors.OKCYAN + f"{df.loc[mask, 'Name'].values[0]} darf sowieso schon wählen" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + f"Ungültige Eingabe. Namen oder Schülerausweis ID eingeben oder zum Abbrechen 'break' und Wiederwählen 'undo' benutzen." + bcolors.ENDC)

        elif student:
            mask = get_dataframe_rows_from_name(name=student, df=df)
            df_anzeigen = df[mask].reset_index()

            if df_anzeigen.shape[0] == 0:
                print(bcolors.FAIL + f"Kein Schülername beginnt mit '{student}'" + bcolors.ENDC)
                continue
            print("~" * 50)
            print(df_anzeigen[["Name", "Ausweisnummer", "gewaehlt"]])
            print("~" * 50)
            while True:
                nummer = input("Bitte eine Zeilennummer auswählen, oder 'break' zum Abbruch schreiben: ")
                if not nummer.isdigit():
                    if nummer == "break":
                        break
                    else:
                        print(print(bcolors.FAIL + f"Bitte Zahl links vom Namen verwenden" + bcolors.ENDC))
                        continue
                nummer = int(nummer)
                if nummer > df_anzeigen.shape[0] or nummer < 0:
                    print(print(bcolors.FAIL + f"Bitte gültige Zeilennummer auswählen" + bcolors.ENDC))
                    continue

                if df.iloc[df_anzeigen.iloc[nummer]["index"]]["gewaehlt"]:
                    df.iloc[df_anzeigen.iloc[nummer]["index"], df.columns.get_loc('gewaehlt')] = False
                    print(bcolors.OKGREEN + f"{df.iloc[df_anzeigen.iloc[nummer]['index']]['Name']} darf wieder wählen" + bcolors.ENDC)
                    return df

            if nummer == "break":
                continue

counter = 0
df = pd.read_csv("speicher/students.csv", encoding="utf-8-sig")

while True:
    student = receive_input()

    if student == "undo":
        df = undo(df)
        counter += 1
        continue

    elif student == "break":
        dateTimeObj = datetime.now()
        timeObj = dateTimeObj.time()
        timestamp = '%d-%d-%d %d:%d:%d' % (timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)
        df.to_csv(f"Zwischenspeicher_{timestamp}")
        break

    if student.isdigit():
        mask = get_dataframe_row_from_id(id=student, df=df)
        if df[mask].shape[0] == 1:
            if not df.loc[mask, "gewaehlt"].bool():
                df.loc[mask, "gewaehlt"] = True
                print(bcolors.OKGREEN + f"{df.loc[mask, 'Name'].values[0]} darf wählen" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + f"{df.loc[mask, 'Name'].values[0]} hat schon gewählt" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + f"Ungültige Eingabe. Namen oder Schülerausweis ID eingeben oder zum Abbrechen 'break' und Wiederwählen 'undo' benutzen." + bcolors.ENDC)
  

    elif student:
        mask = get_dataframe_rows_from_name(name=student, df=df)
        df_anzeigen = df[mask].reset_index()

        if df_anzeigen.shape[0] == 0:
            print(bcolors.FAIL + f"Kein Schülername beginnt mit '{student}'" + bcolors.ENDC)
            continue
        print(df_anzeigen[["Name", "Ausweisnummer", "gewaehlt"]])

        while True:
            nummer = input("Bitte eine Zeilennummer auswählen, oder 'break' zum Abbruch schreiben: ")
            if not nummer.isdigit():
                if nummer == "break":
                    break
                else:
                    print(print(bcolors.FAIL + f"Bitte Zahl links vom Namen verwenden" + bcolors.ENDC))
                    continue
            nummer = int(nummer)
            if nummer > df_anzeigen.shape[0] or nummer < 0:
                print(print(bcolors.FAIL + f"Bitte gültige Zeilennummer auswählen" + bcolors.ENDC))
                continue

            if not df.iloc[df_anzeigen.iloc[nummer]["index"]]["gewaehlt"]:
                df.iloc[df_anzeigen.iloc[nummer]["index"], df.columns.get_loc('gewaehlt')] = True
                print(bcolors.OKGREEN + f"{df.iloc[df_anzeigen.iloc[nummer]['index']]['Name']} darf wählen" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + f"{df.iloc[df_anzeigen.iloc[nummer]['index']]['Name']} hat schon gewählt" + bcolors.ENDC)
            break

        if nummer == "break":
            continue

    counter += 1
    if counter % 10 == 0:
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime('%Y-%m-%d_%H-%M-%S')
        df.to_csv(f"speicher/Zwischenspeicher_{timestamp}.csv")

