import 'dart:async';
import 'video_model.dart';

/// Abstract service layer for video-related API calls.
/// This acts as a bridge between the UI and the Backend.
class VideoApiService {
  // Singleton pattern for easy access
  static final VideoApiService _instance = VideoApiService._internal();
  factory VideoApiService() => _instance;
  VideoApiService._internal();

  /// Toggles the 'Like' status on the backend.
  /// Currently simulates a successful response after a short delay.
  Future<bool> toggleLike(VideoItem video) async {
    // PLACEHOLDER: Replace with actual HTTP call (e.g., POST /api/videos/{id}/like)
    print('DEBUG: Calling API to toggle Like for Video ID: ${video.id}');
    await Future.delayed(const Duration(milliseconds: 300));
    return true; // Simulate success
  }

  /// Toggles the 'Bookmark' status on the backend.
  Future<bool> toggleBookmark(VideoItem video) async {
    print('DEBUG: Calling API to toggle Bookmark for Video ID: ${video.id}');
    await Future.delayed(const Duration(milliseconds: 300));
    return true;
  }

  /// Toggles the 'Follow' status for a user.
  Future<bool> toggleFollow(String username) async {
    print('DEBUG: Calling API to toggle Follow for User: $username');
    await Future.delayed(const Duration(milliseconds: 300));
    return true;
  }

  /// Submits a comment to the backend.
  Future<bool> postComment(int videoId, String text) async {
    print('DEBUG: Calling API to post comment on Video ID: $videoId - Text: $text');
    await Future.delayed(const Duration(milliseconds: 500));
    return true;
  }
}
