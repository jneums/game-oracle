# Data Dictionary

| Feature | Type | Description | Source |
|---------|------|-------------|--------|
| id | Integer | Database primary key | Database |
| Name    | String | Original Title | RAWG API |
| RawgID | Integer | RAWG unique ID | RAWG API |
| SteamURL | String | Steam URL | Steam |
| Metacritic | Integer | Games metacritic rating | RAWG API |
| Genres | String | Genres associated with game | Steam |
| Indie | Boolean | Whether or not the game was created by indie developers | Steam |
| Presence | Integer | Number of posts on social media sights e.g. Reddit | RAWG API |
| Platform | String | Which platforms the game was built to run on | RAWG API |
| RatingsBreakdown | String | Percent of ratings that were good, medium, or bad | RAWG API |
| ReleaseDate | String | When the game was released | RAWG API |
| Soundtrack | Boolean | Whether or not the game has been tagged for a notable soundtrack | Steam |
| Franchise | Boolean | Is the game part of a larger franchise | Steam |
| OriginalCost | Float | How much in USD the game cost at release | Steam |
| DiscountedCost | Float | How much the game costs currently in USD | Steam |
| Players | String | Single-player, multi-player, split-screen, etc | Steam |
| Controller | Boolean | Whether or not the game can be played with a controller | Steam |
| ESRB | String | Recommended appropriate age and type of inappropriate content | RAWG API |
| Achievements | Integer | How many achievements can be earned in game | RAWG API |
| Publisher | String | Companies responsible for publishing the game | RAWG API |
| Languages | String | Which languages are available in-game | Steam |
| Graphics | String | Required GPU for running the game | Steam |
| Storage | Integer | How much storage space is required to download the game | Steam |
| Memory | Integer | How much memory is required to support the game | Steam |
| Tags | String | User generated tags for describing game | Steam |
| Description | String | How the game developer describes the game | RAWG API |
