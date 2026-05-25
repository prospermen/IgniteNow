// VideoItem model to hold video metadata and social metrics
class VideoItem {
  final int id;
  final String videoUrl;
  final String description;
  final String username;
  final String songName;
  final String likes;
  final String comments;
  final String bookmarks;

  VideoItem({
    required this.id,
    required this.videoUrl,
    required this.description,
    required this.username,
    required this.songName,
    required this.likes,
    required this.comments,
    required this.bookmarks,
  });
}

// Mock data source for testing the video feed with social data
final List<VideoItem> mockVideoList = [
  VideoItem(
    id: 1,
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-tree-with-yellow-leaves-low-angle-shot-4725-large.mp4',
    description: 'Beautiful tree with yellow leaves #nature #autumn',
    username: 'nature_lover',
    songName: 'Original Audio - Nature Sounds',
    likes: '125.4K',
    comments: '1.2K',
    bookmarks: '12K',
  ),
  VideoItem(
    id: 2,
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-young-woman-with-a-red-mask-on-her-face-3243-large.mp4',
    description: 'Stay safe everyone! #redmask #style',
    username: 'mask_fashion',
    songName: 'Masked Up - Remix',
    likes: '89.2K',
    comments: '850',
    bookmarks: '5K',
  ),
  VideoItem(
    id: 3,
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-mother-with-her-little-daughter-eating-a-marshmallow-4322-large.mp4',
    description: 'Sweet moments with my daughter #family #love',
    username: 'mom_diaries',
    songName: 'Sweet Heart - Lullaby',
    likes: '250.1K',
    comments: '3.4K',
    bookmarks: '45K',
  ),
  VideoItem(
    id: 4,
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-girl-in-neon-lighting-in-the-rain-31358-large.mp4',
    description: 'Cyberpunk vibes in the rain #neon #vibes',
    username: 'neon_rider',
    songName: 'Electric Dreams - Synthwave',
    likes: '45.6K',
    comments: '420',
    bookmarks: '2.3K',
  ),
];
