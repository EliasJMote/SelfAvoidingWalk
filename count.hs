#!/usr/bin/env stack
{- stack
    --resolver lts-12.21
    script
    --package aeson
    --package bytestring
    --package containers
    --package text
-}
{-# LANGUAGE OverloadedStrings, DeriveGeneric #-}

import Data.Aeson
import qualified Data.ByteString.Lazy.Char8 as L8
import Data.List
import Data.Set (Set, elems, fromList)
import qualified Data.Text as T
import Control.Applicative
import Control.Monad
import GHC.Generics

data Symbol = Symbol T.Text deriving (Show, Generic, Eq)
instance Ord Symbol where
  compare (Symbol a) (Symbol b) = compare a b
instance FromJSON Symbol
instance ToJSON Symbol

data State = State Int deriving (Show, Generic, Eq)
instance Ord State where
  compare (State a) (State b) = compare a b
instance FromJSON State
instance ToJSON State

data DFA =
  DFA { symbols     :: !(Set Symbol)
      , states      :: !(Set State)
      , transitions :: ![[Maybe State]]
      , start       :: !State
      , final       :: !(Set State)
      } deriving (Show, Generic)
instance FromJSON DFA
instance ToJSON DFA

-- | Generate a transition matrix from a delta function
tabulate :: (State -> Symbol -> Maybe State) -> Set State -> Set Symbol -> [[Maybe State]]
tabulate δ qs ss = map (\q -> map (δ q) $ elems ss) $ elems qs

-- A DFA for testing purposes
myDFA :: DFA
myDFA = DFA { symbols = myΣ, states = myQ, transitions = tabulate myδ myQ myΣ, start = mys, final = myF }
  where
    myΣ :: Set Symbol
    myΣ = fromList $ map Symbol ["a", "b", "c", "d"]

    myQ :: Set State
    myQ = fromList $ map State [0, 1, 2, 3, 4]

    myδ :: State -> Symbol -> Maybe State
    myδ (State s) _ = Just $ State (s + 1)

    mys :: State
    mys = State 0

    myF :: Set State
    myF = fromList $ map State [4]

main :: IO ()
main = do
  putStrLn $ "Encode: " ++ show (encode myDFA)
  putStrLn $ "Decode: " ++ show (decode "{\"transitions\":[[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]],\"states\":[0,1,2,3,4],\"final\":[4],\"symbols\":[\"a\",\"b\",\"c\",\"d\"],\"start\":0}" :: Maybe DFA)
  L8.putStrLn $ encode myDFA
