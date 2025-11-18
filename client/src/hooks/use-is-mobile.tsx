import * as React from "react"

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    const checkMobile = () => {
      const hasTouchScreen = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
      const hasCoarsePointer = window.matchMedia('(pointer: coarse)').matches;
      const isNarrowScreen = window.innerWidth < 768;
      
      return hasTouchScreen || hasCoarsePointer || isNarrowScreen;
    }
    
    const mql = window.matchMedia('(pointer: coarse)')
    const onChange = () => {
      setIsMobile(checkMobile())
    }
    
    mql.addEventListener("change", onChange)
    setIsMobile(checkMobile())
    
    return () => mql.removeEventListener("change", onChange)
  }, [])

  return !!isMobile
}
