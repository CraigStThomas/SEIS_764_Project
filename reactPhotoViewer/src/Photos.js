import React, { useCallback, useEffect, useState } from "react";

export default function Photos() {
  const [imageNumber, setImageNumber] = useState("00");
  const [intervalValue, setIntervalValue] = useState(500);
  const IMAGE_FAMILIES = ["A01", "A02", "A03", "A04", "A05", "A06"];
  const [imageFamily, setImageFamily] = useState(IMAGE_FAMILIES[0]);
  const [imageSrc, setImageSrc] = useState(
    require(`../../images/${imageFamily}/${imageNumber}_${imageFamily}_blended.png`)
  );
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    setImageSrc(
      require(`../../images/${imageFamily}/${imageNumber}_${imageFamily}_blended.png`)
    );
  }, [imageFamily, imageNumber]);

  const handleSetImageNumber = useCallback(imageInt => {
    function handleSetImageNumber(imageInt) {
     if (imageInt >= 1 && imageInt <= 788) {
       const newImageString = imageInt.toString().length < 2 ? `0${imageInt}` : `${imageInt}`;
         imageInt <= 788 ? setImageNumber(newImageString) : setImageNumber('00');
     } else {
       setImageNumber('00');
     }
   }
   handleSetImageNumber(+imageInt);
  }, [])

  const handleIncrementImageNumber = useCallback(() => {
    function handleIncrementImageNumberInner() {
      const imageInt = +imageNumber + 1;
      handleSetImageNumber(imageInt);
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
    };
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
    setImageFamily(e.target.value);
  }

  return (
    <>
      <div>
        <button onClick={handleTogglePause}>Toggle Pause</button>
        <label style={{ padding: "10px" }}>
          Milliseconds per frame:
          <input onChange={handleSetIntervalValue} value={intervalValue} />
        </label>
        <label style={{ padding: "10px" }}>
          Image family:
          <select onChange={handleSetImageFamily} value={imageFamily}>
            {IMAGE_FAMILIES.map(imageFamily => {
              return (
                <option key={imageFamily} value={imageFamily}>
                  {imageFamily}
                </option>
              );
            })}
          </select>
        </label>
        <label style={{ padding: "10px" }}>
          Image number:
          <input
            onChange={e => handleSetImageNumber(e.target.value)}
            value={imageNumber}
          />
        </label>
      </div>
      <div>{`${imageNumber}_${imageFamily}_blended.png`}</div>
      <img
        style={{ maxWidth: "90vw", maxHeight: "90vh" }}
        src={imageSrc}
        alt="imageSrc"
      />
    </>
  );
}
