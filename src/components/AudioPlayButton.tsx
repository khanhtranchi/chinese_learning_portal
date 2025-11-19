import React, { useEffect, useRef, useState } from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './AudioPlayButton.module.css';

interface AudioPlayButtonProps {
  src: string;
  autoPlayToken?: number;
}

export default function AudioPlayButton({
  src,
  autoPlayToken,
}: AudioPlayButtonProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);
  
  // Sử dụng useBaseUrl để xử lý baseUrl đúng cách
  const audioSrc = useBaseUrl(src);

  const handlePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      audio.currentTime = 0;
      setIsPlaying(false);
    } else {
      audio.play().catch((error) => {
        console.error('Error playing audio:', error);
        setHasError(true);
        setIsPlaying(false);
      });
      setIsPlaying(true);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
  };

  const handleError = () => {
    console.error('Audio load error:', audioSrc);
    setHasError(true);
    setIsPlaying(false);
  };

  useEffect(() => {
    if (autoPlayToken === undefined || autoPlayToken === 0) {
      return;
    }
    const audio = audioRef.current;
    if (!audio) {
      return;
    }
    audio.pause();
    audio.currentTime = 0;
    setHasError(false);
    setIsPlaying(false);

    const playAudio = () => {
      audio
        .play()
        .then(() => {
          setIsPlaying(true);
        })
        .catch((error) => {
          console.error('Error auto-playing audio:', error);
          setHasError(true);
          setIsPlaying(false);
        });
    };

    if (
      audio.readyState >= HTMLMediaElement.HAVE_ENOUGH_DATA ||
      audio.buffered.length > 0
    ) {
      playAudio();
      return;
    }

    const handleCanPlay = () => {
      audio.removeEventListener('canplaythrough', handleCanPlay);
      playAudio();
    };

    audio.addEventListener('canplaythrough', handleCanPlay);
    audio.load();

    return () => {
      audio.removeEventListener('canplaythrough', handleCanPlay);
    };
  }, [autoPlayToken]);

  // Nếu có lỗi, không hiển thị button
  if (hasError) {
    return null;
  }

  return (
    <>
      <audio
        ref={audioRef}
        src={audioSrc}
        preload="none"
        onEnded={handleEnded}
        onError={handleError}
      />
      <button
        className={styles.playButton}
        onClick={handlePlay}
        aria-label="Play audio"
        type="button"
      >
        {isPlaying ? '⏸️' : '▶️'}
      </button>
    </>
  );
}

