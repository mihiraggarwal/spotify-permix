# spotify-permix

A CLI based tool to save your Daily Mix playlists on Spotify as your own playlist permanently.

## Releases

<a href='https://github.com/mihiraggarwal/spotify-permix/releases/download/v1.0/spotify_permix.exe' target=_blank>v1.0</a>

## Features

- Permanently save any of your Daily Mix playlists before they get updated.
- Distinguish between the saved Daily Mix playlists by date given in the title.

## Setup

- Download the executable folder from releases.
- Run permix.exe located inside the folder.

### Ways to execute

- Using Explorer - Double Click on permix.exe located inside the downloaded folder.
- Using CLI - Go to the path inside the directory and run `permix.exe`.
  
Using CLI, the playlist number can also be passed as an argument, or it can be put as a separate input when prompted.

For example, the following two snippets perform the same function:
```
>>> permix.exe 1
```
```
>>> permix.exe
Enter the number of the Daily Mix playlist which you want saved (1/2/3/4/5/6): 1
```

## Prerequisites

Following/liking the Daily Mix playlist which needs to be saved.

## Configuration

```
>>> permix.exe
Enter the number of the Daily Mix playlist which you want saved (1/2/3/4/5/6): 1
Enter your spotify uri: spotify:user:<username>
Enter the URL you were redirected to: <redirect_url>
Successful!
```

## Subsequent uses

```
>>> permix.exe
Enter the number of the Daily Mix playlist which you want saved (1/2/3/4/5/6): 1
Successful!
```

## Troubleshooting

- In case the playlist isn't found, unfollow the playlist and follow it again.
- Once in a while, it may take more than one execution to be successful.
