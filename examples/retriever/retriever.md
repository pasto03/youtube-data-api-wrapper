## Retriever 
A set of modules that receives different iterable keywords such as channelId or videoId, and return raw items that is extracted from API call response.

Can be intepreted as simplified version of API call.


## Pipes
### Roles of pipe:
1. directly create API client
2. Generate arguments for API call
3. obtain results in loop, and
4. organize API response

### We have two types of pipe:
#### 1. UniquePipe: One id(channelId or videoId) corresponding to one response item
- detail of a channel or video
#### 2. IterablePipe: One id(channelId, playlistId) or parameter(search keyword) corresponding to multiple response item
- playlists under a channel
- search result of one keyword

## PipeSettings
Settings that only applicable to IterablePipe. Determine how many pages of response to be obtained.

&nbsp;
### Check corresponding examples to have inspect of the modules.


### Note: developerKey can be obtained from Google Developer Console