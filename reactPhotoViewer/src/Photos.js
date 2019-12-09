import React, { useCallback, useEffect, useState } from 'react';

export default function Photos() {
  const [imageNumber, setImageNumber] = useState('0');
  const [intervalValue, setIntervalValue] = useState(500);
  const [imageFamily, setImageFamily] = useState('A01');
  // const [imageSrc, setImageSrc] = useState(require(`./img/${imageNumber}_${imageFamily}_blended.png`));
  const [imageSrc, setImageSrc] = useState(require(`../../images/${imageFamily}/${imageNumber}_${imageFamily}_blended.png`));
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    setImageSrc(require(`../../images/${imageFamily}/${imageNumber}_${imageFamily}_blended.png`));
  }, [imageFamily, imageNumber])

  const handleSetImageNumber = useCallback(imageInt => {
    function handleSetImageNumber(imageInt) {
     if (imageInt >= 1 && imageInt <= 788) {
       const newImageString = imageInt.toString().length < 2 ? `${imageInt}` : `${imageInt}`;
         imageInt <= 788 ? setImageNumber(newImageString) : setImageNumber('0');
     }
   }
   handleSetImageNumber(imageInt);
  }, [])

  const handleIncrementImageNumber = useCallback(() => {
    function handleIncrementImageNumberInner() {
      const imageInt = +imageNumber + 1;
      handleSetImageNumber(imageInt)
    }
    handleIncrementImageNumberInner();
  }, [handleSetImageNumber, imageNumber]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (!isPaused) {
        handleIncrementImageNumber();
      }
    }, intervalValue);

    return () => {
      clearInterval(interval);
    }
  }, [isPaused, intervalValue, handleIncrementImageNumber]);

  function handleTogglePause() {
    setIsPaused(!isPaused);
  }

  function handleSetIntervalValue(e) {
    if (!isPaused) {
      handleTogglePause();
    }
    setIntervalValue(e.target.value);
  }

  function handleSetImageFamily(e) {
    if (!isPaused) {
      handleTogglePause();
    }
    if (['A01', 'A02', 'A03', 'A04', 'A05', 'A06'].includes(e.target.value)) {
      setImageFamily(e.target.value)
    }
  }

  return (
    <>
      <div>
        <button onClick={handleTogglePause}>Toggle Pause</button>
        <input onChange={handleSetIntervalValue}/>
        <input onChange={handleSetImageFamily}/>
        <input onChange={e => handleSetImageNumber(e.target.value)}/>
      </div>
      <div>{`${imageNumber}_${imageFamily}_blended.png`}</div>
      <img style={{maxWidth: '90vw', maxHeight: '90vh'}} src={imageSrc} alt="imageSrc"/>
    </>
  )
}
