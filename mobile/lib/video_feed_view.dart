import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'video_model.dart';
import 'video_pool_manager.dart';
import 'video_widgets.dart';

class VideoFeedView extends StatefulWidget {
  const VideoFeedView({super.key});

  @override
  State<VideoFeedView> createState() => _VideoFeedViewState();
}

class _VideoFeedViewState extends State<VideoFeedView> {
  late VideoPoolManager _poolManager;
  final PageController _pageController = PageController();

  @override
  void initState() {
    super.initState();
    _poolManager = VideoPoolManager(videos: mockVideoList);
    // Initialize the first batch
    _poolManager.updateIndex(0);
  }

  @override
  void dispose() {
    _poolManager.dispose();
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // 1. Video Layer
          PageView.builder(
            scrollDirection: Axis.vertical,
            controller: _pageController,
            itemCount: mockVideoList.length,
            onPageChanged: (index) {
              setState(() {
                _poolManager.updateIndex(index);
              });
            },
            itemBuilder: (context, index) {
              final controller = _poolManager.getController(index);
              final video = mockVideoList[index];

              return Stack(
                fit: StackFit.expand,
                children: [
                  // Video Player
                  if (controller != null && controller.value.isInitialized)
                    GestureDetector(
                      onTap: () {
                        setState(() {
                          controller.value.isPlaying
                              ? controller.pause()
                              : controller.play();
                        });
                      },
                      child: Center(
                        child: AspectRatio(
                          aspectRatio: controller.value.aspectRatio,
                          child: VideoPlayer(controller),
                        ),
                      ),
                    )
                  else
                    const Center(
                      child: CircularProgressIndicator(color: Colors.white),
                    ),

                  // 2. Right Side Actions (Heart, Comment, etc.)
                  Positioned(
                    right: 12,
                    bottom: 0,
                    top: 0,
                    child: RightSideActions(video: video),
                  ),

                  // 3. Bottom Info (Username, Song, etc.)
                  Positioned(
                    left: 12,
                    bottom: 20,
                    right: 80,
                    child: BottomInfo(video: video),
                  ),
                ],
              );
            },
          ),

          // 4. Top Navigation (Tabs & Search)
          const TopNavigation(),
        ],
      ),
      // 5. App Bottom Navigation Bar
      bottomNavigationBar: const MainBottomNav(),
    );
  }
}
