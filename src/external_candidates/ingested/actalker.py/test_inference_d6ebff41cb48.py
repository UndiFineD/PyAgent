# Extracted from: C:\DEV\PyAgent\.external\ACTalker\test_inference.py
#!/usr/bin/env python
"""
Test script for ACTalker inference functionality
"""

import sys
import os
from omegaconf import OmegaConf

def test_config_loading():
    """Test if config loading works with model paths"""
    try:
        config = OmegaConf.load('config/inference.yaml')
        print("✓ Config loaded successfully")
        
        # Check if model_paths section exists
        if hasattr(config, 'model_paths'):
            print("✓ model_paths section found")
            print(f"  - Whisper model: {config.model_paths.whisper_model}")
            print(f"  - RIFE model: {config.model_paths.rife_model}")
            print(f"  - BFR enhance model: {config.model_paths.bfr_enhance_model}")
            print(f"  - Face align base dir: {config.model_paths.face_align_base_dir}")
        else:
            print("❌ model_paths section not found")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_imports():
    """Test if all necessary modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import torch
        import cv2
        import numpy as np
        from diffusers import AutoencoderKLTemporalDecoder
        from transformers import WhisperModel
        print("✓ Basic imports successful")
        
        # Test ACTalker specific imports
        from src.utils.util import seed_everything
        from src.models.audio_adapter.audio_proj import AudioProjModel
        print("✓ ACTalker imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_assets():
    """Test if required assets exist"""
    required_files = [
        'assets/ref.jpg',
        'assets/audio.mp3', 
        'assets/video.mp4',
        'config/inference.yaml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✓ All required assets found")
        return True

def main():
    print("🧪 ACTalker Inference Test\n")
    
    tests = [
        ("Config Loading", test_config_loading),
        ("Module Imports", test_imports), 
        ("Required Assets", test_assets),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to run inference.")
        print("\n📝 Next step:")
        print("Run: CUDA_VISIBLE_DEVICES=7 python Inference.py --config config/inference.yaml --ref assets/ref.jpg --audio assets/audio.mp3 --video assets/video.mp4 --mode 2")
        return True
    else:
        print("\n❌ Some tests failed. Please fix issues before running inference.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 