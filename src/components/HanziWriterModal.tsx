import React, { useEffect, useRef, useState } from 'react';
// @ts-ignore - hanzi-writer không có type definitions
import HanziWriter from 'hanzi-writer';
import styles from './HanziWriterModal.module.css';

interface HanziWriterModalProps {
  character: string;
  isOpen: boolean;
  onClose: () => void;
}

export default function HanziWriterModal({
  character,
  isOpen,
  onClose,
}: HanziWriterModalProps) {
  const writerRef = useRef<any>(null);
  const targetRef = useRef<HTMLDivElement>(null);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (!isOpen || !targetRef.current) return;

    // Tạo HanziWriter instance
    try {
      writerRef.current = HanziWriter.create(targetRef.current, character, {
        width: 300,
        height: 300,
        padding: 10,
        showOutline: true,
        strokeColor: '#000000',
        radicalColor: '#ff0000',
      });
    } catch (error) {
      console.error('Error creating HanziWriter:', error);
      return;
    }

    // Tự động phát animation khi mở
    setIsAnimating(true);
    writerRef.current.animateCharacter({
      onComplete: () => setIsAnimating(false),
    });

    return () => {
      if (writerRef.current) {
        writerRef.current = null;
      }
    };
  }, [character, isOpen]);

  const handleReplay = () => {
    if (writerRef.current) {
      setIsAnimating(true);
      writerRef.current.animateCharacter({
        onComplete: () => setIsAnimating(false),
      });
    }
  };

  const handleQuiz = () => {
    if (writerRef.current) {
      setIsAnimating(true);
      writerRef.current.quiz({
        onComplete: () => setIsAnimating(false),
        onMistake: (strokeData) => {
          console.log('Mistake on stroke:', strokeData);
        },
      });
    }
  };

  if (!isOpen) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>
          ✕
        </button>
        <h3 className={styles.title}>Cách viết: {character}</h3>
        <div ref={targetRef} className={styles.writerContainer} />
        <div className={styles.controls}>
          <button
            className={styles.button}
            onClick={handleReplay}
            disabled={isAnimating}
          >
            🔄 Xem lại
          </button>
          <button
            className={styles.button}
            onClick={handleQuiz}
            disabled={isAnimating}
          >
            ✏️ Luyện viết
          </button>
        </div>
      </div>
    </div>
  );
}

