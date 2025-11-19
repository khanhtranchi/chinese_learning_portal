import React, { useEffect, useRef, useState } from 'react';
// @ts-ignore - hanzi-writer không có type definitions
import HanziWriter from 'hanzi-writer';
import styles from './HanziWriterModal.module.css';

interface HanziWriterModalProps {
  character: string;
  isOpen: boolean;
  onClose: () => void;
  onSave?: (char: string) => void;
  title?: string;
}

export default function HanziWriterModal({
  character,
  isOpen,
  onClose,
  onSave,
  title,
}: HanziWriterModalProps) {
  const writerRef = useRef<any>(null);
  const targetRef = useRef<HTMLDivElement>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [hasCompletedQuiz, setHasCompletedQuiz] = useState(false);
  const [isOutlineVisible, setIsOutlineVisible] = useState(false);
  const isFillMode = Boolean(onSave);

  useEffect(() => {
    if (!isOpen || !targetRef.current) return;

    targetRef.current.innerHTML = '';
    setHasCompletedQuiz(false);
    setIsOutlineVisible(false);

    try {
      writerRef.current = HanziWriter.create(targetRef.current, character, {
        width: 300,
        height: 300,
        padding: 10,
        showOutline: false,
        showCharacter: false,
        strokeColor: '#000000',
        radicalColor: '#ff0000',
        highlightOnComplete: true,
        showHintAfterMisses: 2,
      });
    } catch (error) {
      console.error('Error creating HanziWriter:', error);
      return;
    }

    writerRef.current.hideCharacter?.();
    writerRef.current.hideOutline?.();

    if (!isFillMode) {
      setIsBusy(true);
      writerRef.current.animateCharacter({
        onComplete: () => setIsBusy(false),
      });
    } else {
      setHasCompletedQuiz(false);
      writerRef.current.quiz({
        onComplete: () => {
          setHasCompletedQuiz(true);
        },
        onMistake: (strokeData: any) => {
          console.log('Mistake on stroke:', strokeData);
        },
      });
    }

    return () => {
      if (writerRef.current) {
        writerRef.current.cancelQuiz?.();
        writerRef.current.hideCharacter?.();
        writerRef.current.hideOutline?.();
      writerRef.current = null;
      }
      if (targetRef.current) {
        targetRef.current.innerHTML = '';
      }
    };
  }, [character, isOpen, isFillMode]);

  const handleReplay = () => {
    if (!writerRef.current) return;
    setIsBusy(true);
    writerRef.current.animateCharacter({
      onComplete: () => setIsBusy(false),
    });
  };

  const handleToggleOutline = () => {
    if (!writerRef.current) return;
    if (isOutlineVisible) {
      writerRef.current.hideOutline?.();
      setIsOutlineVisible(false);
    } else {
      writerRef.current.showOutline?.();
      setIsOutlineVisible(true);
    }
  };

  const handleSave = () => {
    if (!onSave) return;
    onSave(character);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>
          ✕
        </button>
        <h3 className={styles.title}>
          {title || `Cách viết: ${character}`}
        </h3>
        {isFillMode && (
          <p className={styles.helperText}>
            Hãy vẽ đủ nét rồi lưu chữ này vào chỗ trống. Bạn có thể bật gợi ý
            viền nếu cần.
          </p>
        )}
        <div ref={targetRef} className={styles.writerContainer} />
        {isFillMode && (
          <div className={styles.statusMessage}>
            {hasCompletedQuiz ? '✅ Đã hoàn thành nét viết' : '✏️ Chưa hoàn thành bài viết'}
          </div>
        )}
        <div className={styles.controls}>
          <button className={styles.button} onClick={handleToggleOutline}>
            {isOutlineVisible ? '🙈 Ẩn gợi ý' : '💡 Gợi ý'}
          </button>
          {!isFillMode && (
            <button
              className={styles.button}
              onClick={handleReplay}
              disabled={isBusy}
            >
              🔄 Xem lại
            </button>
          )}
          {isFillMode ? null : (
            <button
              className={styles.button}
              onClick={() => writerRef.current?.quiz()}
              disabled={isBusy}
            >
              ✏️ Luyện viết
            </button>
          )}
          {isFillMode && onSave && (
            <button
              className={`${styles.button} ${styles.primaryButton}`}
              onClick={handleSave}
              disabled={!hasCompletedQuiz}
            >
              💾 Lưu vào chỗ trống
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

