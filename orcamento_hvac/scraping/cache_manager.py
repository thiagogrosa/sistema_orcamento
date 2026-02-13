"""
Gerenciador de cache para resultados de scraping.
"""
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

from .config import CACHE_DIR, CACHE_EXPIRY_HOURS


class CacheManager:
    """Gerencia cache de resultados de scraping."""

    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, url: str, scraper_name: str) -> str:
        """Gera chave única para cache baseada na URL e scraper."""
        key_str = f"{scraper_name}:{url}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Retorna caminho do arquivo de cache."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, url: str, scraper_name: str, max_age_hours: int = CACHE_EXPIRY_HOURS) -> Optional[Dict[str, Any]]:
        """
        Recupera dados do cache se válidos.

        Args:
            url: URL que foi scrapeda
            scraper_name: Nome do scraper
            max_age_hours: Idade máxima do cache em horas

        Returns:
            Dados do cache ou None se expirado/inexistente
        """
        cache_key = self._get_cache_key(url, scraper_name)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Verificar validade
            cached_at = datetime.fromisoformat(data['cached_at'])
            age = datetime.now() - cached_at

            if age > timedelta(hours=max_age_hours):
                return None

            return data

        except (json.JSONDecodeError, KeyError, ValueError):
            # Cache corrompido, remover
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, url: str, scraper_name: str, data: Dict[str, Any]) -> None:
        """
        Armazena dados no cache.

        Args:
            url: URL que foi scrapeda
            scraper_name: Nome do scraper
            data: Dados para cachear
        """
        cache_key = self._get_cache_key(url, scraper_name)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            'url': url,
            'scraper': scraper_name,
            'cached_at': datetime.now().isoformat(),
            'data': data
        }

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def clear_expired(self, max_age_hours: int = CACHE_EXPIRY_HOURS) -> int:
        """
        Remove caches expirados.

        Args:
            max_age_hours: Idade máxima em horas

        Returns:
            Número de caches removidos
        """
        removed = 0
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        for cache_file in self.cache_dir.glob('*.json'):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                cached_at = datetime.fromisoformat(data['cached_at'])
                if cached_at < cutoff:
                    cache_file.unlink()
                    removed += 1

            except (json.JSONDecodeError, KeyError, ValueError):
                # Cache corrompido, remover
                cache_file.unlink()
                removed += 1

        return removed

    def clear_all(self) -> int:
        """Remove todos os caches. Retorna número de arquivos removidos."""
        removed = 0
        for cache_file in self.cache_dir.glob('*.json'):
            cache_file.unlink()
            removed += 1
        return removed

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        cache_files = list(self.cache_dir.glob('*.json'))
        total_size = sum(f.stat().st_size for f in cache_files)

        ages = []
        for cache_file in cache_files:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cached_at = datetime.fromisoformat(data['cached_at'])
                age = (datetime.now() - cached_at).total_seconds() / 3600
                ages.append(age)
            except:
                pass

        return {
            'total_files': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'avg_age_hours': sum(ages) / len(ages) if ages else 0,
            'oldest_hours': max(ages) if ages else 0,
            'newest_hours': min(ages) if ages else 0
        }
