# Custom CAH

## Tärkeää
Jos olet kirjautunut sisään ennen ja kohtaat paljon virheitä, poista evästeet ja kirjaudu uudelleen. Eräs session parametrin nimi on muuttunut painovirheen takia ja session tyhjentäminen korjaa virheet.

## Projektin kuvaus
Sovelluksen tavoitteena on luoda alusta, jolla käyttäjät voivat luoda räätälöityjä kortteja Cards Against Humanity -peliin.
Sovelluksen toiminnallisuuteen tulisi kuulua mahdollisuus rekisteröityä ja kirjautua sisään, luoda omia korttipakkoja ja lisätä sinne kortteja.
Luodessaan pakkaa käyttäjän on määritettävä nimi, kieli ja yksityisyysasetukset. Yksityiset pakat eivät ole muiden kuin käyttäjän nähtävissä,
kun taas julkisia näkyvät vapaasti kaikille pääsivulla, käyttäjän tilillä ja haussa.

Suunniteltuihin toimintoihin kuuluu myös mahdollisuus jättää arvosanoja julkisille pakoille.
Käyttäjä voi myös testata pakkejaan yksin simulaatiopelissä, jossa häntä pyydetään täydentämään yksi musta kortti pakastaan yhdellä kymmenestä satunnaisesta
valkoisesta kortista sekoittamalla pakkaa joka kerta.

## Mikä on valmista:
- Käyttäjä voi rekisteröityä ja kirjautua sisään. Kahdella käyttäjällä ei voi olla samaa nimi, vaikka ne olisi kirjoitettu eri kokoisilla kirjaimilla. Turvallisuuden vuoksi salasanat myös hashataan, ja sovellus käyttää csrf-tunnuksia istunnon tunnistamiseen.
- Käyttäjä voi kirjautua omaan profiiliin ja katsella muiden profiileja. Sovelluksessa on haku, jossa on mahdollista etsiä toisten ihmisten julkisia pakkoja. Toisaalta, jos henkilö ei julkaissut mitään, hänen sivulle pääsee vain jos tietää hänen nimensä ja kirjoittaa sen manuaalisesti osoiteriville.
- Sivujen sisältö muuttuu hieman: esimerkiksi jos käyttäjää ei ole olemassa, jos kyseessä on oma tai jonkun toisen profiili.
- Käyttäjä voi profiilissaan luoda pakkoja, antaa niille nimen, kielen ja määrittää yksityisyyden.
- Pakat tallennetaan tietokantaan ja näytetään sitten profiilissa. Julkiset pakat ovat kaikkien nähtävissä, kun taas yksityiset pakat näkyvät vain omistajalle.
- On mahdollista siirtyä pakan sivulle, jossa näkyy tietoja siitä. Käyttäjä voi luoda valkoisia tai mustia kortteja pakassaan.
- Käyttäjä voi muokata pakan tiedot tai poistaa sitä kokonaan. Sen lisäksi on mahdollista muokata tai poistaa kortteja.
- Käyttäjä voi jättää arvosteluja toisille pakoille, myös omalle. Kommenttien ikkunassa näkyy, jos jokin kommentti on omistajan lisäämä. Omia kommentteja pystyy muokkaamaan tai poistamaan.
- On yksinkertainen haku, joka etsii pakkoja nimen, omistajan tai kielen perusteella.
- Sovelluksessa on yksinkertainen ulkoasu.
- Pääsivulla näkyy kaikki uudet julkaissut pakat.
- On yksinkertainen pelisimulaattori, jossa voi testata pakkoja.

Sovellus on saatavilla [Fly.io:ssa](https://custom-cah.fly.dev)
