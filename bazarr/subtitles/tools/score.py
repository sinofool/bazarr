# coding=utf-8

from __future__ import annotations

import logging

from app.config import get_settings

logger = logging.getLogger(__name__)

class Score:
    media = None
    defaults = {}

    def __init__(self, load_profiles=False, **kwargs):
        self.data = self.defaults.copy()
        self.data.update(**kwargs)
        self.data["hash"] = self._hash_score()
        self._profiles = []
        self._profiles_loaded = False

        if load_profiles:
            self.load_profiles()

    def check_custom_profiles(self, subtitle, matches):
        if not self._profiles_loaded:
            self.load_profiles()

        for profile in self._profiles:
            if profile.check(subtitle):
                matches.add(profile.name)

    def load_profiles(self):
        self._profiles = []

        if self._profiles:
            logger.debug("Loaded profiles: %s", self._profiles)
        else:
            logger.debug("No score profiles found")
            self._profiles = []

        self._profiles_loaded = True

    def reset(self):
        self.data.update(self.defaults)

    def update(self, **kwargs):
        self.data.update(kwargs)

    @classmethod
    def from_config(cls, **kwargs):
        return cls(True, **kwargs)

    def get_scores(self, min_percent, special=None):
        return (
            self.max_score * (special or min_percent) / 100,
            self.max_score,
            set(list(self.scores.keys())),
        )

    @property
    def custom_profile_scores(self):
        return {item.name: item.score for item in self._profiles}

    @property
    def scores(self):
        return {**self.custom_profile_scores, **self.data}

    @property
    def max_score(self):
        return (
            self.data["hash"]
            + self.data["hearing_impaired"]
            + sum(item.score for item in self._profiles if item.score)
        )

    def _hash_score(self):
        return sum(
            val
            for key, val in self.data.items()
            if key not in ("hash", "hearing_impaired")
        )

    def __str__(self):
        return f"<{self.media} Score class>"


class SeriesScore(Score):
    media = "series"
    defaults = {
        "hash": 359,
        "series": 180,
        "year": 90,
        "season": 30,
        "episode": 30,
        "release_group": 15,
        "source": 7,
        "audio_codec": 3,
        "resolution": 2,
        "video_codec": 2,
        "hearing_impaired": 1,
        "streaming_service": 0,
        "edition": 0,
    }

    @classmethod
    def from_config(cls, **kwargs):
        return cls(True, **kwargs["series_scores"])

    def update(self, **kwargs):
        self.data.update(kwargs["series_scores"])


class MovieScore(Score):
    media = "movies"
    defaults = {
        "hash": 119,
        "title": 60,
        "year": 30,
        "release_group": 15,
        "source": 7,
        "audio_codec": 3,
        "resolution": 2,
        "video_codec": 2,
        "hearing_impaired": 1,
        "streaming_service": 0,
        "edition": 0,
    }

    @classmethod
    def from_config(cls, **kwargs):
        return cls(True, **kwargs["movie_scores"])

    def update(self, **kwargs):
        self.data.update(kwargs["movie_scores"])


series_score = SeriesScore.from_config(**get_settings())
movie_score = MovieScore.from_config(**get_settings())
