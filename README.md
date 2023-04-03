# custom-cards

Sovelluksen tavoitteena on luoda alusta, jolla käyttäjät voivat luoda räätälöityjä kortteja Cards Against Humanity -peliin.
Sovelluksen toiminnallisuuteen tulisi kuulua mahdollisuus rekisteröityä ja kirjautua sisään, luoda omia mukautettuja korttipakkoja ja lisätä sinne omia kortteja.
Luodessaan pakkaa käyttäjän on määritettävä nimi, kieli ja yksityisyysasetukset. Yksityiset pakat eivät ole muiden kuin käyttäjän nähtävissä,
kun taas julkisia ovat vapaasti nähtävissä. Tulevaisuudessa pitäisi olla mahdollista etsiä julkisia paketteja tiettyjen parametrien perusteella.

Suunniteltuihin toimintoihin kuuluu myös mahdollisuus jättää arvosanoja julkisille pakoille.
Käyttäjä voi myös testata pakkejaan yksin simulaatiopelissä, jossa häntä pyydetään täydentämään yksi musta kortti pakastaan yhdellä kymmenestä satunnaisesta
valkoisesta kortista sekoittamalla pakkaa joka kerta.

Tällä hetkellä näistä ovat valmiina seuraavat ominaisuudet:
- Käyttäjä voi rekisteröityä ja kirjautua sisään. Kahdella käyttäjällä ei voi olla samaa nimi, vaikka ne olisi kirjoitettu eri kokoisilla kirjaimilla. Turvallisuuden vuoksi salasanat myös hashataan, ja sovellus käyttää csrf-tunnuksia istunnon tunnistamiseen.
- Käyttäjä voi kirjautua omaan profiiliin ja katsella muiden profiileja. Sovelluksessa ei kuitenkaan ole vielä hakua, ja toisen henkilön sivulle pääsee vain, jos tietää hänen nimensä ja kirjoittaa sen manuaalisesti osoiteriville.
- Sivujen sisältö muuttuu hieman: esimerkiksi jos käyttäjää ei ole olemassa, jos kyseessä on oma tai jonkun toisen profiili.
- Käyttäjä voi profiilissaan luoda pakkoja, antaa niille nimen, kielen ja määrittää yksityisyyden.
- Pakat tallennetaan tietokantaan ja näytetään sitten profiilissa. Julkiset pakkaukset ovat kaikkien nähtävissä, kun taas yksityiset pakkaukset näkyvät vain omistajalle.

Mikä ei ole vielä valmista:
- On mahdollista siirtyä pakan sivulle, jossa näkyy tietoja siitä. Korttien luominen pakoissa ei kuitenkaan ole vielä mahdollista.
- Pakettien muokkaaminen tai poistaminen ei ole mahdollista, vaikka sivulle on lisätty joitakin painikkeita.
- (Jos esimerkiksi haluat muokata paketin nimeä ja napsautat painiketta, sinut ohjataan yksinkertaisesti pääsivulle.)
- Ei voi jättää arvioita ja kommentteja toisille pakoille.
- Pelisimulaattoria ei ole.
- Käyttäjiä tai pakkoja ei voi etsiä.
- Sovelluksessa ei ole mitään ulkoasua, vain pelkkää html-koodi.
