import 'package:video_player/video_player.dart';
import 'video_model.dart';

class VideoPoolManager {
  final List<VideoItem> videos;
  final Map<int, VideoPlayerController> _controllers = {};
  
  // Current active index in the PageView
  int _currentIndex = 0;

  VideoPoolManager({required this.videos});

  /// Updates the sliding window based on the new index.
  /// Initializes neighbors and disposes controllers outside the range [index-1, index+1].
  void updateIndex(int newIndex) {
    _currentIndex = newIndex;
    
    // Indices that should be in memory
    final Set<int> activeIndices = {
      newIndex - 1,
      newIndex,
      newIndex + 1
    }.where((i) => i >= 0 && i < videos.size).toSet();

    // 1. Dispose controllers no longer in the sliding window
    final List<int> toDispose = _controllers.keys
        .where((i) => !activeIndices.contains(i))
        .toList();

    for (var index in toDispose) {
      _controllers[index]?.dispose();
      _controllers.remove(index);
    }

    // 2. Initialize controllers for the current window
    for (var index in activeIndices) {
      _ensureControllerInitialized(index);
    }

    // 3. Manage playback
    _handlePlayback(newIndex);
  }

  void _ensureControllerInitialized(int index) {
    if (!_controllers.containsKey(index)) {
      final controller = VideoPlayerController.networkUrl(
        Uri.parse(videos[index].videoUrl),
      );
      _controllers[index] = controller;
      controller.initialize().then((_) {
        // Force refresh if this is the current video and it finished initializing
        if (index == _currentIndex) {
          controller.play();
          controller.setLooping(true);
        }
      });
    }
  }

  void _handlePlayback(int activeIndex) {
    _controllers.forEach((index, controller) {
      if (index == activeIndex) {
        if (controller.value.isInitialized) {
          controller.play();
          controller.setLooping(true);
        }
      } else {
        controller.pause();
      }
    });
  }

  VideoPlayerController? getController(int index) {
    return _controllers[index];
  }

  void dispose() {
    for (var controller in _controllers.values) {
      controller.dispose();
    }
    _controllers.clear();
  }
}

extension on List {
  int get size => length;
}
