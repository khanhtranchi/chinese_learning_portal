import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import AudioPlayButton from '../AudioPlayButton';
import FillInBlankCharacter from '../FillInBlankCharacter';
import styles from './ExerciseSection.module.css';

type ExerciseItem = {
  id: string;
  type: 'dialogue' | 'chunk';
  text_cn: string;
  pinyin: string;
  translation?: string;
  meaning?: string;
  speaker?: string;
  audio: string;
  mask: number[];
  length: number;
};

type ExerciseSectionProps = {
  lessonId: string;
  audioBase: string;
  data: {
    dialogues: ExerciseItem[];
    chunks: ExerciseItem[];
  };
};

const shuffleList = (items: ExerciseItem[]): ExerciseItem[] => {
  const clone = [...items];
  for (let i = clone.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [clone[i], clone[j]] = [clone[j], clone[i]];
  }
  return clone;
};

export default function ExerciseSection({
  lessonId,
  audioBase,
  data,
}: ExerciseSectionProps) {
  const {
    siteConfig: { baseUrl = '/' },
  } = useDocusaurusContext();
  const [includeDialogues, setIncludeDialogues] = useState(true);
  const [includeChunks, setIncludeChunks] = useState(true);
  const [started, setStarted] = useState(false);
  const [queue, setQueue] = useState<ExerciseItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [blankStatus, setBlankStatus] = useState<Record<string, boolean>>({});
  const [cycle, setCycle] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [autoPlayToken, setAutoPlayToken] = useState(0);
  const preloadedRef = useRef<Set<string>>(new Set());

  const resolveAudioUrl = useCallback(
    (src: string) => {
      if (!src) {
        return '';
      }
      if (src.startsWith('http://') || src.startsWith('https://')) {
        return src;
      }
      if (src.startsWith('/')) {
        return `${baseUrl.replace(/\/+$/, '')}${src}`;
      }
      return `${baseUrl}${src}`;
    },
    [baseUrl],
  );

  const currentExercise = useMemo(
    () => (started && queue.length > 0 ? queue[currentIndex] : null),
    [started, queue, currentIndex],
  );

  const resetForExercise = useCallback((exercise: ExerciseItem | null) => {
    if (!exercise) {
      setBlankStatus({});
      setShowHint(false);
      return;
    }
    const map: Record<string, boolean> = {};
    exercise.mask.forEach((_, idx) => {
      map[`${exercise.id}-${idx}`] = false;
    });
    setBlankStatus(map);
    setShowHint(false);
    setCycle((prev) => prev + 1);
    setAutoPlayToken((prev) => prev + 1);
  }, []);

  const handleFilledChange = useCallback((blankKey: string, filled: boolean) => {
    setBlankStatus((prev) => {
      if (prev[blankKey] === filled) {
        return prev;
      }
      return { ...prev, [blankKey]: filled };
    });
  }, []);

  const totalBlanks = currentExercise?.mask.length ?? 0;
  const blanksFilled =
    totalBlanks === 0
      ? true
      : currentExercise?.mask.every(
          (_, idx) => blankStatus[`${currentExercise.id}-${idx}`],
        ) ?? false;

  const canProceed = started && currentExercise ? blanksFilled : false;

  const handleStart = () => {
    const pool = [
      ...(includeDialogues ? data.dialogues : []),
      ...(includeChunks ? data.chunks : []),
    ];
    if (pool.length === 0) {
      setStatusMessage('Vui lòng chọn ít nhất một loại bài tập.');
      return;
    }
    const shuffled = shuffleList(pool);
    setQueue(shuffled);
    setCurrentIndex(0);
    setStarted(true);
    setStatusMessage(null);
    resetForExercise(shuffled[0] ?? null);
  };

  const handleNext = () => {
    if (!currentExercise) {
      return;
    }
    const isLast = currentIndex === queue.length - 1;
    if (isLast) {
      const reshuffled = shuffleList(queue);
      setQueue(reshuffled);
      setCurrentIndex(0);
      resetForExercise(reshuffled[0] ?? null);
      return;
    }
    const nextIndex = currentIndex + 1;
    setCurrentIndex(nextIndex);
    resetForExercise(queue[nextIndex]);
  };

  useEffect(() => {
    if (!started || queue.length === 0) {
      return;
    }
    queue.forEach((item) => {
      const resolved = resolveAudioUrl(item.audio);
      if (!resolved || preloadedRef.current.has(resolved)) {
        return;
      }
      const audio = new Audio(resolved);
      audio.preload = 'auto';
      audio.load();
      preloadedRef.current.add(resolved);
    });
  }, [started, queue, resolveAudioUrl]);

  const renderText = (exercise: ExerciseItem) => {
    if (!exercise) {
      return null;
    }
    const chars = Array.from(exercise.text_cn);
    const maskSet = new Set(exercise.mask);
    let blankOrdinal = 0;
    return chars.map((char, idx) => {
      if (maskSet.has(idx)) {
        const blankKey = `${exercise.id}-${blankOrdinal}`;
        const key = `${blankKey}-${cycle}`;
        blankOrdinal += 1;
        return (
          <FillInBlankCharacter
            key={key}
            answer={char}
            onFilledChange={(filled) => handleFilledChange(blankKey, filled)}
          />
        );
      }
      return (
        <span key={`${exercise.id}-char-${idx}`} aria-hidden="true">
          {char}
        </span>
      );
    });
  };

  return (
    <section
      className={styles.section}
      data-lesson={lessonId}
      data-audio-base={audioBase}
    >
      <div className={styles.controls}>
        <label className={styles.checkboxGroup}>
          <input
            type="checkbox"
            checked={includeDialogues}
            onChange={(e) => setIncludeDialogues(e.target.checked)}
          />
          Hội thoại
        </label>
        <label className={styles.checkboxGroup}>
          <input
            type="checkbox"
            checked={includeChunks}
            onChange={(e) => setIncludeChunks(e.target.checked)}
          />
          Cụm từ
        </label>
        <button
          type="button"
          className={styles.startButton}
          onClick={handleStart}
        >
          Start
        </button>
        {statusMessage && (
          <span className={styles.statusMessage}>{statusMessage}</span>
        )}
      </div>

      {!started && (
        <p className={styles.noExercise}>
          Chọn loại bài tập và nhấn Start để bắt đầu luyện tập.
        </p>
      )}

      {started && currentExercise && (
        <div className={styles.exerciseCard}>
          <div className={styles.exerciseMeta}>
            <span className={styles.pill}>
              {currentExercise.type === 'dialogue' ? 'Hội thoại' : 'Cụm từ'}
            </span>
            <span>
              Câu {currentIndex + 1}/{queue.length}
            </span>
          </div>

          <div className={styles.charactersLine}>
            {renderText(currentExercise)}
          </div>

          <div className={styles.actions}>
            <div className={styles.audioButtonWrapper}>
              <AudioPlayButton
                src={currentExercise.audio}
                autoPlayToken={autoPlayToken}
              />
            </div>
            <button
              type="button"
              className={styles.hintButton}
              onClick={() => setShowHint((prev) => !prev)}
            >
              {showHint ? 'Ẩn hint' : 'Hint'}
            </button>
            <button
              type="button"
              className={styles.nextButton}
              onClick={handleNext}
              disabled={!canProceed}
            >
              Next
            </button>
          </div>

          {showHint && (
            <div className={styles.hintArea}>
              <div className={styles.hintText}>{currentExercise.pinyin}</div>
              {currentExercise.type === 'chunk' && currentExercise.meaning && (
                <div className={styles.hintText}>{currentExercise.meaning}</div>
              )}
              {currentExercise.type === 'dialogue' &&
                currentExercise.translation && (
                  <div className={styles.hintText}>
                    {currentExercise.translation}
                  </div>
                )}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

