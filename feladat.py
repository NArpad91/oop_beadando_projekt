from datetime import datetime, timedelta
import sys
from abc import ABC, abstractmethod

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, szobsz, ar):
        self.szobsz = szobsz
        self.ar = ar

# Származtatott osztályok az absztrakt Szoba osztályból
class EgyagyasSzoba(Szoba):
    def __init__(self, szobsz, bath):
        super().__init__(szobsz, 50000)  # Ár per nap
        self.bath = bath

class KetagyasSzoba(Szoba):
    def __init__(self, szobsz, extra):
        super().__init__(szobsz, 80000)  # Ár per nap
        self.extra = extra

class LuxusSzoba(Szoba):
    def __init__(self, szobsz, felszereltség):
        super().__init__(szobsz, 120000)  # Ár per nap
        self.felszereltség = felszereltség

# Foglalás osztály
class Foglalas:
    def __init__(self, szoba, kezdeti_datum, veg_datum):
        self.szoba = szoba
        self.kezdeti_datum = kezdeti_datum
        self.veg_datum = veg_datum

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.fgs_ok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def elerheto_szobak(self, szoba_tipus, kezdeti_datum, veg_datum):
        elerheto = []
        for szoba in self.szobak:
            if isinstance(szoba, szoba_tipus):
                foglalt = any(fgs.szoba == szoba and not (fgs.veg_datum < kezdeti_datum or fgs.kezdeti_datum > veg_datum) for fgs in self.fgs_ok)
                if not foglalt:
                    elerheto.append(szoba)
        return elerheto

    def fgs(self, szoba, kezdeti_datum, veg_datum):
        if kezdeti_datum < datetime.now() or veg_datum < kezdeti_datum:
            print("\nHibás dátumok! A foglalás csak jövőbeni időpontra lehetséges és a kezdeti dátum nem lehet későbbi, mint a végdátum.")
            sys.stdout.write('\a')
            sys.stdout.flush()
            return None
        napok_szama = (veg_datum - kezdeti_datum).days + 1
        total_ar = szoba.ar * napok_szama
        self.fgs_ok.append(Foglalas(szoba, kezdeti_datum, veg_datum))
        print(f"Sikeres foglalás! Szobaszám: {szoba.szobsz}, Időtartam: {kezdeti_datum.strftime('%Y-%m-%d')} - {veg_datum.strftime('%Y-%m-%d')}, Teljes ár: {total_ar} Ft")
        return total_ar

    def lmond(self, szobsz):
        for fgs in list(self.fgs_ok):
            if fgs.szoba.szobsz == szobsz:
                self.fgs_ok.remove(fgs)
                print(f"A foglalás sikeresen lemondva: Szobaszám: {szobsz}")
                return True
        print("Nincs ilyen szobaszámú foglalás.")
        return False

    def list_fgs_ok(self):
        sorted_fgs = sorted(self.fgs_ok, key=lambda x: x.kezdeti_datum)
        for fgs in sorted_fgs:
            print(f"Szoba: {fgs.szoba.szobsz}, Időtartam: {fgs.kezdeti_datum.strftime('%Y-%m-%d')} - {fgs.veg_datum.strftime('%Y-%m-%d')}")

# Szálloda és szobák inicializálása
hotel = Szalloda("Relax Inn")
hotel.add_szoba(EgyagyasSzoba("101", "Zuhany"))
hotel.add_szoba(KetagyasSzoba("102", "Mini bár"))
hotel.add_szoba(LuxusSzoba("201", "Jacuzzi és szauna"))

# Felhasználói interfész
while True:
    print("\nVálassz műveletet:")
    print("1. Szoba foglalása")
    print("2. Foglalás lemondása")
    print("3. Foglalások listázása")
    print("4. Szobák listázása")
    print("5. Kilépés")
    case = input("Művelet kiválasztása (1/2/3/4/5): ")

    if case == "1":
        print("\nVálassza ki a szoba típusát:")
        print("1. Egyágyas Szoba")
        print("2. Ketagyas Szoba")
        print("3. Luxus Szoba")
        szoba_tipus_valasztas = input("Kérem a szoba típusát (1/2/3): ")
        szoba_tipus = {1: EgyagyasSzoba, 2: KetagyasSzoba, 3: LuxusSzoba}.get(int(szoba_tipus_valasztas), None)

        if not szoba_tipus:
            print("\nHibás választás!")
            continue

        kezdeti_datum = input("Add meg a foglalás kezdeti dátumát (ÉÉÉÉ-HH-NN): ")
        veg_datum = input("Add meg a foglalás végdátumát (ÉÉÉÉ-HH-NN): ")
        try:
            kezdeti_datum = datetime.strptime(kezdeti_datum, "%Y-%m-%d")
            veg_datum = datetime.strptime(veg_datum, "%Y-%m-%d")
            elerheto_szobak = hotel.elerheto_szobak(szoba_tipus, kezdeti_datum, veg_datum)
            if not elerheto_szobak:
                print("\nNincsenek elérhető szobák ebben az időszakban.")
                continue

            print("\nElérhető szobák:")
            for szoba in elerheto_szobak:
                print(f"Szobaszám: {szoba.szobsz}, Ár: {szoba.ar} Ft/nap")

            szobsz = input("Válassz szobaszámot a foglaláshoz: ")
            kivalasztott_szoba = next((s for s in elerheto_szobak if s.szobsz == szobsz), None)
            if not kivalasztott_szoba:
                print("\nHibás szobaszám!")
                continue

            hotel.fgs(kivalasztott_szoba, kezdeti_datum, veg_datum)
        except ValueError:
            print("\nHibás dátum formátum!")
            sys.stdout.write('\a')
            sys.stdout.flush()

    elif case == "2":
        szobsz = input("\nAdd meg a lemondandó foglalás szoba számát: ")
        hotel.lmond(szobsz)

    elif case == "3":
        hotel.list_fgs_ok()

    elif case == "4":
        print("\nSzobák listázása:")
        for szoba in hotel.szobak:
            if isinstance(szoba, EgyagyasSzoba):
                print(f"Egyágyas Szoba: {szoba.szobsz}, Ár: {szoba.ar} Ft/nap, Fürdő: {szoba.bath}")
            elif isinstance(szoba, KetagyasSzoba):
                print(f"Ketagyas Szoba: {szoba.szobsz}, Ár: {szoba.ar} Ft/nap, Extra: {szoba.extra}")
            elif isinstance(szoba, LuxusSzoba):
                print(f"Luxus Szoba: {szoba.szobsz}, Ár: {szoba.ar} Ft/nap, Felszereltség: {szoba.felszereltség}")

    elif case == "5":
        break
    else:
        print("\nHibás választás!")
        sys.stdout.write('\a')
        sys.stdout.flush()
