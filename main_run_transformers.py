from dotenv import load_dotenv
from ai_datahive.transformers import DailyTrendingGithubProjectTransformer, TopDailyImageTransformer, \
    DailyArxivPaperTransformer, TopDailyImageCritiqueTransformer



def main():
    load_dotenv()
    github_repos_transformer = DailyTrendingGithubProjectTransformer()
    github_repos_transformer.run()

    images_transformer = TopDailyImageTransformer()
    images_transformer.run()

    images_crit_transformer = TopDailyImageCritiqueTransformer()
    images_crit_transformer.run()

    arxiv_papers_transformer = DailyArxivPaperTransformer()
    arxiv_papers_transformer.run()


if __name__ == '__main__':
    main()
