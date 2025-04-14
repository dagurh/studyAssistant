Inngangur, hvaðan kom hugmynd.
Hugmyndin kom í raun út frá raunverulegu vandamáli þar sem kæratan mín glósar mjög mikið úr fyrirlestrum og notar stundum chatGPT til að búa til samantekt yfir glósurnar og mér fannst það bara fínt tækifæri á að búa til eitthvað sem hún gæti mögulega nýtt sér.

Útfærsla, hvaða skilyrði eru uppfyllt og afhverju.
Þetta verkefni uppfyllir þessi helstu skylirði fyrir vefþjónustu.
  - CRUD virkni (create, read, update, delete)
  - API endapunkta fyrir glósur, samantektir og prófaspurningar
  - Tenging við MongoDB
  - Noktun á OpenAI API til að búa til samantektir og prófaspurningar
  - Notendaumsjón

Tækni, hvaða tækni er notuð og afhverju.
 - FastAPI: Mjög þæginlegt framwork, auðvelt að byggja REST API og það býður upp á sjálfvirka skjölun á endapunktum
 - MongoDB: NoSQL gagnagrunnur, mjög sveigjanlegur. Kom sér vel fyrir upp á það að taka á móti svörum frá OpenAI API.
 - OpenAI: Notað til að búa til samantektir og prófspurningar úr glósum.
 - Pydantic: Sjá til þess að gögnin sem eru send með body og query í hverri beiðni eru rétt og örugg
 - Pytest: Notað í sjálfvirkar prófanir á vefþjónustunni
 - REST client (VSCode extention): Notað fyrir beiðnir á endapunkta

Hvað gekk vel.
Uppsetningin sjálf gekk mjög vel og það kom á óvart hvað það er þæginlegt að nota FastAPI. Þetta er mjög vel documentað framework og auðvelt að koma sér af stað. Það gekk líka vel að setja upp hvaða gögn má senda inn með hverju kalli þar sem pydantic er með innbyggðan klasa sem heitir BaseModel sem maður notar til að skilgreina lögleg gögn.

Hvað gekk illa.
Til að byrja með gekk mjög illa að prófa að senda inn beiðnir á endapunkta, ég fór í gegnum Postman, Insomnia og Hoppscotch, var alltaf að fá mismunandi hegðun frá hverju og einu varðandi beiðnir. Endaði svo að rekast á REST client og lenti ekki í neinu veseni eftir það.
Ég átti líka í smá basli með að senda inn og taka út gögn frá MongoDB vegna þess að mongoDB býr sjálfkrafa til id sem object id sem tók mig smá tíma að leysa í byrjun.

Hvað var áhugavert.
Það var áhugavert að nota OpenAI API og gefa því rétta skipun til þess að skila einhverju frá sér á þæginlegu JSON formatti. Ég lenti í smá stríði við það á tímapunkti

Framhaldið.
Ég vil byggja framenda sem notar þennan API. Framendinn verður byggður í React og sett fram á einkaléni. Þar verður bæði hægt að skoða demo af vefsíðunni ásamt því að búa til aðgang og nota hana eins og ætlað er.
