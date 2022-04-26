# yt-playlist-improved
source: https://github.com/modkhi/yt-playlist
A YouTube playlist downloader. Requires [Python 3.6+](https://www.python.org/downloads/), [pytube](https://github.com/nficano/pytube), and [ffmpeg](https://www.ffmpeg.org/) to work.

This script will download the audio of every song in a YouTube playlist, then convert the audio to mp3. To use, place it in the folder in which you want to download the playlist.

If got error message "pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple" or "AttributeError: 'NoneType' object has no attribute 'span'", try replace the function get_throttling_function_name in ../lib/python3.x/site-packages/pytube/cipher.py with:


    def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.
    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # a.C&&(b=a.get("n"))&&(b=Dea(b),a.set("n",b))}};
        # In above case, `Dea` is the relevant function name
        r'a\.[A-Z]&&\(b=a\.get\("n"\)\)&&\(b=([^(]+)\(b\)',
    ]
    logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            logger.debug("finished regex search, matched: %s", pattern)
            function_name = function_match.group(1)
            is_Array = True if '[' or ']' in function_name else False
            if is_Array:
                index = int(re.findall(r'\d+', function_name)[0])
                name = function_name.split('[')[0]
                pattern = r"var %s=\[(.*?)\];" % name
                regex = re.compile(pattern)
                return regex.search(js).group(1).split(',')[index]
            else:
                return function_name

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )
