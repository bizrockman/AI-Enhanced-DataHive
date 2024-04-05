from dotenv import load_dotenv
from ai_datahive.collectors import CivitaiCollector, ArxivCollector, GithubCollector


def main():
    load_dotenv()

    civitai_image_loader = CivitaiCollector(creator='CivitAIDailyTopImage', media_type='image', period='Day',
                                            nsfw_level=None, limit=3)
    civitai_image_loader.run()
    civitai_hot_image_loader = CivitaiCollector(creator='CivitAIDailyTopHotImage', media_type='image',
                                                period='Day', nsfw_level='Mature', limit=3)
    civitai_hot_image_loader.run()
    github_repos_loader = GithubCollector()
    github_repos_loader.run()
    arxiv_papers_loader = ArxivCollector()
    arxiv_papers_loader.run()


if __name__ == '__main__':
    main()
