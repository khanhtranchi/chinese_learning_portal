import React, { useEffect, useMemo, useState } from 'react';
import HanziWriterModal from './HanziWriterModal';
import styles from './FillInBlankCharacter.module.css';

interface FillInBlankCharacterProps {
  answer: string;
  placeholder?: string;
  hint?: string;
  onFilledChange?: (filled: boolean) => void;
}

export default function FillInBlankCharacter({
  answer,
  placeholder = '___',
  hint,
  onFilledChange,
}: FillInBlankCharacterProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [filledChar, setFilledChar] = useState<string | null>(null);

  const displayValue = useMemo(
    () => filledChar || placeholder,
    [filledChar, placeholder],
  );

  useEffect(() => {
    onFilledChange?.(Boolean(filledChar));
  }, [filledChar, onFilledChange]);

  return (
    <span className={styles.wrapper}>
      <button
        type="button"
        className={`${styles.blankButton} ${
          filledChar ? styles.blankButtonFilled : ''
        }`}
        onClick={() => setIsModalOpen(true)}
        aria-label={
          filledChar
            ? `Đã điền chữ ${filledChar}, bấm để luyện viết lại`
            : 'Chưa điền chữ, bấm để luyện viết'
        }
      >
        <span
          className={
            filledChar ? styles.filledValue : styles.placeholderValue
          }
        >
          {displayValue}
        </span>
      </button>
      {hint && <small className={styles.hint}>{hint}</small>}
      <HanziWriterModal
        character={answer}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={(char) => setFilledChar(char)}
        title="Điền chữ vào chỗ trống"
      />
    </span>
  );
}

