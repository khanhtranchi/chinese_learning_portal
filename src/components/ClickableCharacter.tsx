import React, { useState } from 'react';
import HanziWriterModal from './HanziWriterModal';
import styles from './ClickableCharacter.module.css';

interface ClickableCharacterProps {
  char: string;
  pinyin?: string;
  meaning?: string;
  children?: React.ReactNode;
}

export default function ClickableCharacter({
  char,
  pinyin,
  meaning,
  children,
}: ClickableCharacterProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsModalOpen(true);
  };

  return (
    <>
      <span
        className={styles.clickableChar}
        onClick={handleClick}
        title={`Click để xem cách viết: ${char}`}
      >
        {children || char}
      </span>
      <HanziWriterModal
        character={char}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
}

