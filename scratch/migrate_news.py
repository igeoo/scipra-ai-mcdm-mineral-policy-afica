import os

articles = [
    {
        "filename": "News_Article_1.txt",
        "title": "Lonmin accused of prolonging platinum strike by hiding revenue",
        "content": "South African platinum producer Lonmin, which was crippled by a five-month strike this year, could have met workers’ wage demands, had it not moved revenue through a Bermudan subsidiary, a lobby group has said. The world’s third-biggest platinum miner has moved earnings from South Africa to low-tax Bermuda using a unit called Western Platinum since at least 2006, the Cape Town-based Alternative Information and Development Centre (AIDC) said in a 41-page report."
    },
    {
        "filename": "News_Article_2.txt",
        "title": "Marikana massacre: The first of Lonmin's voices are heard",
        "content": "The Lonmin manager, with his executive committee’s blessing, had previously agreed to speak directly to rock drill operators. Recent pay advances at Impala and Amplats forced Lonmin to acknowledge they were paying their drillers less than other the platinum mines and knew they had to address it or face losing these vital workers to their competitors."
    },
    {
        "filename": "News_Article_3.txt",
        "title": "Families of slain Marikana mine workers reflect on decade of betrayal",
        "content": "As the country prepares to remember that horrific day 10 years ago, the victims’ families tell Daily Maverick of their sense of betrayal and justice not served. Ntombizolile Mosepetsane, whose husband was killed, says: “It’s like we don’t exist. No one from the government or the mine has come to say sorry.”"
    },
    {
        "filename": "News_Article_4.txt",
        "title": "Marikana: Lonmin defends housing plan",
        "content": "Lonmin has defended its progress on building houses for its employees, saying it has met its social and labour plan obligations despite financial constraints. The company stated that the slow pace of housing was due to the 2014 strike and the slump in platinum prices."
    },
    {
        "filename": "News_Article_5.txt",
        "title": "Marikana tragedy has changed industry forever",
        "content": "The Marikana tragedy has fundamentally altered the South African mining landscape. The rise of AMCU and the decline of NUM's dominance has led to a new era of labor relations characterized by higher wage demands and increased volatility. Investors are reassessing the risk profile of the PGM sector."
    },
    {
        "filename": "News_Article_6.txt",
        "title": "Mining cost pressures to impact negatively on employees",
        "content": "Increasing electricity costs, labor demands, and declining productivity are putting the South African mining industry under severe pressure. Analysts warn that these factors could lead to further job losses and mine closures if a sustainable solution is not found."
    },
    {
        "filename": "News_Article_7.txt",
        "title": "Sibanye's $286 million Lonmin takeover gets all clear from shareholders",
        "content": "Sibanye-Stillwater and Lonmin cleared the final hurdle to forming the world's second-largest platinum producer as their shareholders approved the South African miner's $286 million takeover. The deal was seen as a way to save Lonmin from financial collapse."
    },
    {
        "filename": "News_Article_8.txt",
        "title": "AMCU Marikana commemoration: A decade of struggle",
        "content": "AMCU president Joseph Mathunjwa addressed thousands of workers at the Marikana koppie, calling for continued struggle for a living wage and justice for those killed in 2012. The union remains a powerful force in the platinum belt."
    },
    {
        "filename": "News_Article_9.txt",
        "title": "Lonmin ultimatum extended - violence causes",
        "content": "Lonmin extended its ultimatum for workers to return to work as violence continued in the Marikana area. Unions argued that the labor dispute was only one factor in the violence, pointing to deeper social and economic grievances."
    },
    {
        "filename": "News_Article_10.txt",
        "title": "For the platinum industry, Marikana was a ‘mechanisation moment’",
        "content": "The Marikana massacre triggered seismic changes in the platinum industry. It is now leaner and more profitable, with a focus on mechanisation. While workers are safer, there are fewer of them, and capital has an edge over labour."
    }
]

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

for art in articles:
    filepath = os.path.join(RAW_DIR, art['filename'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {art['title']}\n\n{art['content']}")
    print(f"Created {filepath}")
