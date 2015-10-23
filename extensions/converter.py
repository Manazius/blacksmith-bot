# BS mark.1-55
# coding: utf-8

#  BlackSmith mark.1
#  converter.py

#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]
#-extmanager-extVer:0.8-# 

CrDesc = {
	"time": { # Время
		"year": 1.0, # Год !# Base (Базовое Значение)
		"month": 12.0, # Месяц
		"week": 52.1785714286, # Неделя
		"day": 365.25, # День
		"hour": 8766.0, # Час
		"minute": 525960.0, # Минута
		"second": 31557600.0, # Секунда
					},
	"information": { # Информация
		"bit": 1.0, # Бит !# Base
		"kbit": 9.765625e-04, # 2^10
		"mbit": 9.53674316406e-07, # 2^20
		"gbit": 9.31322574615e-10, # 2^30
		"tbit": 9.09494701773e-13, # 2^40
		"pbit": 8.881784197e-16, # 2^50
		"ebit": 8.67361737988e-19, # 2^60
		"zbit": 8.47032947254e-22, # 2^70
		"ybit": 8.27180612553e-25, # 2^80
		"byte": 0.125, # Байт
		"kbyte": 1.220703125e-04, # 2^10
		"mbyte": 1.19209289551e-07, # 2^20
		"gbyte": 1.16415321827e-10, # 2^30
		"tbyte": 1.13686837722e-13, # 2^40
		"pbyte": 1.11022302463e-16, # 2^50
		"ebyte": 1.08420217249e-19, # 2^60
		"zbyte": 1.05879118407e-22, # 2^70
		"ybyte": 1.03397576569e-25, # 2^80
					},
	"m.field": { # Магнитное Поле
		"gauss": 1.0, # Gauss; Ггаусс (G; Гс) !# Base
		"tesla": 1e-04, # Tesla; Тесла (T; Тл)
		"ktesla": 1e-07, # 10^03
		"mtesla": 1e-10, # 10^06
		"gtesla": 1e-13, # 10^09
		"ttesla": 1e-16, # 10^12
		"ptesla": 1e-19, # 10^15
		"etesla": 1e-22, # 10^18
		"ztesla": 1e-25, # 10^21
		"ytesla": 1e-28, # 10^24
		"militesla": 1e-01, # 10^-03
		"microtesla": 1e02, # 10^-06
		"nanotesla": 1e05, # 10^-09
		"picotesla": 1e08, # 10^-12
					},
	"power": { # Мощность
		"watt": 1.0, # Watt; Ватт (W; Вт) !# Base
		"kwatt": 1e-03, # 10^03
		"mwatt": 1e-06, # 10^06
		"gwatt": 1e-09, # 10^09
		"twatt": 1e-12, # 10^12
		"hpwr": 0.0013596216173, # Horse Power; Лошадиная Сила
					},
	"radiation": { # Радиационное Излучение
		"bq": 1.0, # Becquerel; Беккерель (Bq; Бк) !# Base (Базовое Значение)
		"ci": 2.7027e-11, # Curie; Кюри (Ci; Ки)
		"rad": 1e-06, # Radiation Absorbed Dose (rad; Рад)
					},
	"temperature": { # Температура
		"c": ((lambda Numb: Numb), # °C (Celsius; Цельсий) !# Base
				(lambda Numb: Numb)),
		"f": ((lambda Numb: (Numb * 9.0 / 5.0 + 32.0)), # from Celsius to °F (Fahrenheit; Фаренгейт)
				(lambda Numb: ((Numb - 32.0) * 5.0 / 9.0))), # to Celsius
		"k": ((lambda Numb: (Numb + 273.15)), # from Celsius to K (Kelvin; Кельвин)
				(lambda Numb: (Numb - 273.15))), # to Celsius
		"r": ((lambda Numb: ((Numb + 491.67) * 9.0 / 5.0)), # from Celsius to °R (Rankine; Ранкин)
				(lambda Numb: ((Numb - 491.67) * 5.0 / 9.0))), # to Celsius
		"n": ((lambda Numb: (Numb * 33.0 / 100.0)), # from Celsius to °N (Newton; Ньютон)
				(lambda Numb: (Numb * 100.0 / 33.0))), # to Celsius
		"de": ((lambda Numb: ((100.0 - Numb) * 3.0 / 2.0)), # from Celsius to °De (Delisle; Делиль)
				(lambda Numb: (100.0 - Numb * 2.0 / 3.0))), # to Celsius
		"re": ((lambda Numb: (Numb * 4.0 / 5.0)), # from Celsius to °Re (Reaumur; Реомюр)
				(lambda Numb: (Numb * 5.0 / 4.0))), # to Celsius
		"ro": ((lambda Numb: (Numb * 21.0 / 40.0 + 7.5)), # from Celsius to °Ro (Romer; Рёмер)
				(lambda Numb: ((Numb - 7.5) * 40.0 / 21.0))), # to Celsius
					},
	"pressure": { # Давление
		"atm": 1.0, # Standard Atmosphere; Атмосферное Давление (atm; атм) !# Base
		"bar": 1.01325, # bar; бар
		"pa": 101325.0, # Pascal; Паскаль (Pa; Па)
		"torr": 760.0, # Torr; Миллиметр Ртутного Столба
		"psi": 14.696, # Pound per Square Inch; Фунт на Квадратный Дюйм
					},
	"volume": { # Объем
		"usbushel": 1.0, # U.S. Bushel; Американский Бушель !# Base
		"bushel": 0.968938622, # U.K. Bushel; Имперский Бушель
		"usgallon": 9.30917797, # U.S. Gallon; Американский Галлон
		"gallon": 7.75150897, # U.K. Gallon; Имперский Галлон
		"usquart": 37.2367119, # U.S. Quart; Американская Кварта
		"quart": 31.0060359, # U.K. Quart; Имперская Кварта
		"uspint": 74.4734238, # U.S. Pint; Американская Пинта
		"pint": 62.0120718, # U.K. Pint; Имперская Пинта
		"usounce": 1191.57478, # U.S. Ounce; Американская Унция
		"ounce": 1240.24144, # U.K. Ounce; Имперская Унция
		"oilbarrel": 0.221647095, # Oil Barrel; Нефтяной Баррель
		"drybarrel": 0.3048, # Dry Barrel; Сухой Баррель
		"fluidbarrel": 0.2955, # Fluid Barrel; Жидкий Баррель
		"litre": 35.239072, # Litre; Литр
		"mililitre": 35239.072, # MiliLitre; Милилитр
		"metre^3": 0.035239072, # Cubic Metre; Кубический Метр
		"foot^3": 1.24445608, # Cubic Foot; Кубический Фут
		"inch^3": 2150.42011, # Cubic Inch; Кубический Дюйм
					},
	"weight": { # Масса
		"g": 1.0, # Gram; Грамм !# Base
		"kg": 1e-03, # KiloGram; Килограмм
		"ton": 1e-06, # Ton; Тонна
		"oz": 0.0352739619, # Ounce; Унция
		"ozt": 0.0321507466, # Troyes Ounce; Тройская Унция
		"lb": 0.00220462262, # Pound; Фунт
		"lbt": 0.002679229, # Troyes Pound; Тройский Фунт
		"pd": 6.10482666e-05, # Russian Pood; Пуд
		"carat": 5.0, # Carat; Карат
					},
	"distance": { # Длина
		"angstrom": 1.0, # Angstrom; Ангстрём !# Base
		"nanometre": 1e-01, # 10^-09
		"micrometre": 1e-04, # 10^-06
		"milimetre": 1e-07, # 10^-03
		"centimetre": 1e-08, # 10^-02
		"decimetre": 1e-09, # 10^-01
		"metre": 1e-10, # Metre; Метр
		"kilometre": 1e-13, # 10^03
		"inch": 3.93700787e-09, # Inch; Дюйм
		"foot": 3.2808399e-10, # Fool; Фут
		"yard": 1.0936133e-10, # Yard; Ярд
		"mille": 6.21371192e-14, # Mile; Миля
		"league": 2.07123730667e-14, # League; Лига
		"seamille": 5.39956803e-14, # Sea Mile; Морская Миля
		"verst": 9.37382827e-14, # Verst; Верста
		"au": 6.68458712267e-22, # Astronomical Unit; Астрономическая Единица (средний радиус земной орбиты)
		"ly": 1.05700083402e-26, # Light-Year; Световой Год
		"pc": 3.24077927001e-27, # Parsec; Парсек
					},
	"speed": { # Скорость
		"km/h": 1.0, # KiloMetres per Hour; Километры в Час !# Base
		"m/s": 0.2778, # Metres per Second; Метры в Секунду
		"knot": 0.539956803, # Sea Miles per Hour; Морские Мили в Час (Knot; Узел)
		"mph": 0.621371192, # Miles per Hour; Мили в Час
		"fps": 0.911344415281, # Feet per Second; Футы в Секунду 
		"ls": 9.26566930076e-10, # Light-Speed; Скорость Света
					},
	"angle": { # Угол
		"degree": 1.0, # Degree; Градус ° !# Base
		"second": 3600.0, # Arc Second; Угловая Секунда
		"minute": 60.0, # Arc Minute; Угловая Минута
		"rad": 0.0174532925, # Radians; Радиан
		"turn": 0.00277777777778, # Turn; Оборот
		"gon": 1.111111111111111, # Gradian; Градон
					},
	"square": { # Площадь
		"acre": 1.0, # Acre; Акр !# Base
		"milimetre^2": 4046856420.0, # Square MilliMetre; Квадратный Миллиметр
		"centimetre^2": 40468564.2, # Square CentiMetre; Квадратный Сантиметр
		"metre^2": 4046.85642, # Square Metre; Квадратный Метр
		"inch^2": 6272640.0, # Square Inch; Квадратный Дюйм
		"foot^2": 0.00355591837, # Square Foot; Квадратный Фут
		"mile^2": 0.0015625, # Square Mile; Квадратная Миля
		"verst^2": 0.00355591837, # Square Verst; Квадратная Верста
		"hectare": 0.404685642, # Hectare; Гектар
		"are": 40.4685642, # Are; Ар
		"barn": 4.04685642e31, # Barn; Барн
					},
	"energy": { # Энергия
		"btu": 1.0, # British Thermal Unit; Британская Термическая Единица !# Base
		"mbtu": 1000000.0, # Million British Thermal Unit; Миллион Британских Термических Единиц
		"cal": 252.164401, # Calorie; Калория
		"kcal": 0.252164401, # KiloCalorie; Килокалория
		"erg": 10550558500.0, # Erg; Эрг
		"ev": 6.58514139e20, # Electronvolt; Электронвольт
		"joule": 1055.05585, # Joule (Watt per Second); Джоуль (Ватт Секунда)
		"watt/h": 0.29307107, # Watt per Hour; Ватт Час
		"kwatt/h": 0.00029307107, # KiloWatt per Hour; Киловатт Час
					},
				}

Convert = lambda Desc, Numb, Type, ToType: (CrDesc[Desc][ToType]*(Numb / CrDesc[Desc][Type]))

ConvertTemp = lambda Numb, Type, ToType, Desc = CrDesc["temperature"]: Desc[ToType][0](Desc[Type][1](Numb))

def command_convert(ltype, source, body):
	if body:
		ls = body.split()
		Desc = (ls.pop(0)).lower()
		if CrDesc.has_key(Desc):
			if len(ls) == 3:
				Numb = (ls.pop(0)).lower()
				if check_number(Numb):
					Type = (ls.pop(0)).lower()
					ToType = (ls.pop(0)).lower()
					if CrDesc[Desc].has_key(Type) and CrDesc[Desc].has_key(ToType):
						if Desc == "temperature":
							answer = str(ConvertTemp(float(Numb), Type, ToType))
						else:
							answer = str(Convert(Desc, float(Numb), Type, ToType))
					else:
						answer = "incorrect unit"
				else:
					answer = "this is not a number"
			elif not ls:
				answer = ", ".join(CrDesc[Desc].keys())
			else:
				answer = "incorrect arguments"
		else:
			answer = "incorrect category"
	else:
		answer = ", ".join(CrDesc.keys())
	reply(ltype, source, answer)
	
command_handler(command_convert, 10, "converter")
