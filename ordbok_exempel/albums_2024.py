albums_2024 = [
    {
        "Artist": "Charles Lloyd",
        "Album": "The Sky Will Still Be There Tomorrow",
        "Genre": ["Jazz"],
        "Critic score": 88
    },
    {
        "Artist": "Aaron West & The Roaring Twenties",
        "Album": "In Lieu of Flowers",
        "Genre": ["Indie Rock", "Folk"],
        "Critic score": 85
    },
    {
        "Artist": "The Cure",
        "Album": "Songs of a Lost World",
        "Genre": ["Alternative Rock", "Gothic Rock"],
        "Critic score": 90
    },
    {
        "Artist": "Julian Lage",
        "Album": "Speak To Me",
        "Genre": ["Jazz", "Instrumental"],
        "Critic score": 87
    },
    {
        "Artist": "Charli xcx",
        "Album": "BRAT",
        "Genre": ["Pop", "Electronic"],
        "Critic score": 92
    }
]

# Exempel på hur du skriver ut alla album och deras genrer
for album in albums_2024:
    print(f"{album['Artist']} - {album['Album']} ({', '.join(album['Genre'])}) - Score: {album['Critic score']}")