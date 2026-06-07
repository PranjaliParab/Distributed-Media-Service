"""
He file run kar Member 3 cha code test karayala.
python -m app.services.test_member3
"""
from image_service import resize_image, compress_image, add_watermark
from video_service import compress_video, generate_thumbnail

# --- IMAGE TESTS ---
print("=== IMAGE TESTS ===")


resize_image("uploads/test.jpg", width=800, height=600)
compress_image("uploads/test.jpg", quality=60)
add_watermark("uploads/test.jpg", "© My Group Project")

# --- VIDEO TESTS ---
print("\n=== VIDEO TESTS ===")

# Test video pahije — "uploads/test.mp4" nanav de
compress_video("uploads/test.mp4")
generate_thumbnail("uploads/test.mp4", timestamp="00:00:02")

print("\n✅ Processing completed successfully. All output files have been saved to the 'processed' directory.")